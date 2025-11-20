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


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario vertical")
    clock = pygame.time.Clock()

    player_img = pygame.image.load(join("assets", "mario_statique.png")).convert_alpha()
    player_img = pygame.transform.scale(player_img, (21, 36))
    enemy_img = pygame.image.load(join("assets", "enemy.png"))
    enemy_img = pygame.transform.scale(enemy_img, (52, 33))
    coin_img = pygame.image.load(join("assets", "dollar.png"))

    score = Score()
    player = Player(player_img)
    shield_manager = ShieldManager()
    player.has_shield = False
    enemies = init_platforms_and_enemies(enemy_img, score)

    coin_manager = CoinManager(coin_img, spawn_probability=0.4)

    running = True
    scroll_started = False
    game_over = False
    started = False
    menu = MainMenu()

    while running:
        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                    player.jump()
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    main()
                    return

        if not started:
            i = menu.run(screen)
            running = i != 0
            started = i == 1
        else:
            if not game_over:
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
                    score.add(1)

                    # 🔥 Vitesse en fonction du score
                    # vitesse de base : 1.7
                    # chaque 100 points de score → +0.2 de vitesse
                    speed = 1.7 + 0.0005 * score.value
                    # on limite la vitesse max pour que ça reste jouable
                    speed = min(speed, 5)
                    set_speed(speed)

                    for p in activePlates:
                        p.update()
                    for e in enemies:
                        e.rect.bottom = e.platform_sprite.y

                    enemies = recycle_platforms_and_enemies(enemies, enemy_img, score)
                    coin_manager.update()

                # Collisions pièces
                coin_manager.check_collision(player.rect, score)

                # Collisions ennemis
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
                if scroll_started:
                    score.add(1)

                    shield_manager.update(activePlates, score.value)

                    if shield_manager.check_collision(player):
                        player.has_shield = True
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

            draw_text(screen, f"Score : {score.value}", 30, BLACK, WIDTH / 2, 10)
            draw_text(screen, f"Coins : {coin_manager.collected}", 25, BLACK, WIDTH - 80, 10)

            level = score.value // 300
            speed = 1.7 + 0.1 * level
            speed = min(speed, 3.5)

            draw_text(screen, f"Speed : {round(speed, 2)}", 20, BLACK, WIDTH / 2, 40)

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