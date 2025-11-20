import pygame
from os.path import join

from main_menu import MainMenu
from player import Player
from plateforme import activePlates, set_speed
from coins import *
from constants import *
import utils

from score import Score
from level import init_platforms_and_enemies, recycle_platforms_and_enemies
from shield import ShieldManager, draw_shield_indicator


def draw_text(screen, text, size, color, x, y):
    try:
        font = pygame.font.Font(join("assets", "SuperMario256.ttf"), size)
    except:
        font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def get_speed(score_value: int) -> float:
    """
    Vitesse du jeu en fonction du score.
    Variation très lente :
      - base : 1.7
      - +0.1 de vitesse tous les 1000 points de score
      - vitesse max : 3.0
    """
    return min(1.7 + 0.0001 * score_value, 3.0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario vertical")
    clock = pygame.time.Clock()

    # --- CHARGEMENT IMAGES ---
    player_img = pygame.image.load(join("assets", "mario_statique.png")).convert_alpha()
    player_img = pygame.transform.scale(player_img, (21, 36))

    enemy_img = pygame.image.load(join("assets", "enemy.png"))
    enemy_img = pygame.transform.scale(enemy_img, (52, 33))

    coin_img = pygame.image.load(join("assets", "dollar.png"))

    # ⚠️ NOUVELLE IMAGE DE PAUSE ⚠️
    # Mets un fichier "pause.png" dans assets (par ex. 400x200 px, texte PAUSE)
    pause_img = pygame.image.load(join("assets", "pause.png"))
    pause_img=pygame.transform.scale(pause_img, (800,600))
    pause_rect = pause_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # --- OBJETS PRINCIPAUX ---
    score = Score()
    player = Player(player_img)
    player.has_shield = False

    shield_manager = ShieldManager()
    enemies = init_platforms_and_enemies(enemy_img, score)
    coin_manager = CoinManager(coin_img, spawn_probability=0.4)

    menu = MainMenu()

    running = True
    scroll_started = False
    game_over = False
    started = False
    paused = False   # <<< ÉTAT DE PAUSE

    while running:
        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    # Saut seulement si pas en pause
                    if not paused and event.key in (pygame.K_SPACE, pygame.K_UP):
                        player.jump()
                    # Toggle pause avec ECHAP
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    main()
                    return

        # --- MENU AVANT LE JEU ---
        if not started:
            i = menu.run(screen)
            running = i != 0
            started = i == 1
        else:
            # --- GAME LOGIC ---
            if not game_over and not paused:
                keys = pygame.key.get_pressed()
                moving = False
                if keys[pygame.K_LEFT]:
                    player.left()
                    moving = True
                if keys[pygame.K_RIGHT]:
                    player.right()
                    moving = True

                player.animate(moving)
                player.frontiere()

                old_bottom = player.rect.bottom
                player.update(HEIGHT)

                # Chute = Game Over
                if scroll_started and player.rect.bottom >= HEIGHT:
                    if not menu.muted:
                        pygame.mixer.Sound.play(menu.sound_fail)
                    game_over = True

                # Collisions plateformes
                on_platform_this_frame = False
                if player.vy >= 0:
                    for p in activePlates:
                        plat_rect = pygame.Rect(p.x, p.y, p.image.get_width(), p.image.get_height())
                        if player.rect.right > plat_rect.left and player.rect.left < plat_rect.right:
                            if old_bottom <= plat_rect.top and player.rect.bottom >= plat_rect.top:
                                player.rect.bottom = plat_rect.top
                                player.vy = 0
                                player.is_jumping = [False, False]
                                on_platform_this_frame = True
                                break

                if on_platform_this_frame and not scroll_started:
                    scroll_started = True

                if scroll_started:
                    # Incrémentation du score liée au scroll
                    score.add(1)

                    # Vitesse en fonction du score (variation lente)
                    speed = get_speed(score.value)
                    set_speed(speed)

                    # Mise à jour plateformes et ennemis
                    for p in activePlates:
                        p.update()
                    for e in enemies:
                        e.rect.bottom = e.platform_sprite.y

                    enemies = recycle_platforms_and_enemies(enemies, enemy_img, score)

                    # Mise à jour coins & shield
                    coin_manager.update()
                    shield_manager.update(activePlates, score.value)
                    if shield_manager.check_collision(player):
                        player.has_shield = True

                # Collisions pièces
                coin_manager.check_collision(player.rect, score)

                # Collisions ennemis
                for e in enemies:
                    e.mouvement_uniforme_in_platform()
                    if player.rect.colliderect(e.rect):
                        if player.has_shield:
                            player.has_shield = False
                            enemies.remove(e)
                            break
                        else:
                            if not menu.muted:
                                pygame.mixer.Sound.play(menu.sound_fail)
                            game_over = True
                            break

            # --- DRAW ---
            screen.blit(utils.getBackground(), (0, 0))

            for p in activePlates:
                p.draw(screen)
            for e in enemies:
                screen.blit(e.image, e.rect.topleft)

            coin_manager.draw(screen)
            player.draw(screen)
            shield_manager.draw(screen)

            if player.has_shield:
                draw_shield_indicator(screen, 10, 50)

            # Score, Coins, Speed
            draw_text(screen, f"Score : {score.value}", 30, BLACK, WIDTH / 2, 10)
            draw_text(screen, f"Coins : {coin_manager.collected}", 25, BLACK, WIDTH - 80, 10)

            current_speed = get_speed(score.value)
            draw_text(screen, f"Speed : {round(current_speed, 2)}", 20, BLACK, WIDTH / 2, 40)

            # --- OVERLAY PAUSE ---
            if paused and not game_over:
                # On dessine juste l'image de pause par-dessus
                screen.blit(pause_img, pause_rect)

            # --- GAME OVER ---
            if game_over:
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(150)
                overlay.fill(BLACK)
                screen.blit(overlay, (0, 0))
                draw_text(screen, "GAME OVER", 80, RED, WIDTH / 2, HEIGHT / 2 - 50)
                draw_text(screen, f"Score Final: {score.value}", 40, WHITE, WIDTH / 2, HEIGHT / 2 + 20)
                draw_text(screen, "Appuyez sur ENTREE pour rejouer", 25, WHITE, WIDTH / 2, HEIGHT / 2 + 80)
                pygame.mixer_music.stop()
                pygame.mixer.Sound.stop(menu.sound)

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()