import pygame
import random
from os.path import join
from main_menu import MainMenu
from player import Player
from plateforme import spawnPlateform, activePlates
from ennemies import Enemy
import utils
from constants import *

#FONCTION D'AFFICHAGE DE TEXTE
def draw_text(screen, text, size, color, x, y):
    try:
        font = pygame.font.Font(join("assets", "SuperMario256.ttf"), size)
    except:
        font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x , y)
    screen.blit(text_surface, text_rect)



#fréquence d'apparition des ennemis
n=1700
def create_enemy_on_platform(plateform, enemy_img):
    x_min = plateform.x
    x_max = plateform.x + plateform.image.get_width()
    platform_params = [x_min, x_max, plateform.y]
    enemy = Enemy(enemy_img, platform_params)
    enemy.rect.bottom = plateform.y
    enemy.platform_sprite = plateform
    plateform.enemy = enemy
    return enemy

def init_platforms_and_enemies(enemy_img,score):
    activePlates.clear()
    enemies = []
    y = HEIGHT - 80
    while y > -HEIGHT:
        for k in range(plateforme_par_ligne):
            p = spawnPlateform()
            p.y = y
            # Gestion de sécurité si l'image n'est pas chargée
            try:
                w = p.image.get_width()
            except:
                w = 100
            p.x = random.randint(0, WIDTH - w)

            if score>500:
                     if random.random() < min(0.9,score/n):
                        e = create_enemy_on_platform(p, enemy_img)
                        enemies.append(e)
            else:
                p.enemy = None
        y -= GAP_Y
    return enemies


def recycle_platforms_and_enemies(enemies, enemy_img,score):
    if not activePlates:
        return enemies

    min_y = min(p.y for p in activePlates)
    for p in activePlates:
        if p.y > HEIGHT + 50:
            p.y = min_y - GAP_Y
            try:
                w = p.image.get_width()
            except:
                w = 100
            p.x = random.randint(0, WIDTH - w)
            min_y = p.y
            if p.enemy is not None:
                e = p.enemy
                e.platform_sprite = p
                x_min = p.x
                x_max = p.x + p.image.get_width()
                e.platform = [x_min, x_max, p.y]
                e.rect.bottom = p.y
                e.rect.x = random.randint(x_min, x_max - e.width)
            else:
                if score>500:
                     if random.random() < min(0.9,score/n):
                        e = create_enemy_on_platform(p, enemy_img)
                        enemies.append(e)
    return enemies




def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario vertical")
    clock = pygame.time.Clock()
    #background = utils.getBackground()

    player_img = pygame.image.load(join("assets", "mario_statique.png")).convert_alpha()
    player_img = pygame.transform.scale(player_img, (21, 36))
    enemy_img = pygame.image.load(join("assets", "enemy.png"))
    enemy_img = pygame.transform.scale(enemy_img, (52, 33))

    score = 0
    player = Player(player_img)
    enemies = init_platforms_and_enemies(enemy_img,score)

    running = True
    scroll_started = False
    game_over = False
    started = False
    menu = MainMenu()

    while running:



        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Si le jeu est en cours
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        player.jump()
            # Si c'est Game Over
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
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
                player.update(HEIGHT)

                # Détection Game Over : Chute
                if scroll_started and player.rect.bottom >= HEIGHT:
                    print("GAME OVER : Tu es tombé !")
                    if not menu.muted:
                        pygame.mixer.Sound.play(menu.sound_fail)

                    game_over = True

                on_platform_this_frame = False
                for p in activePlates:
                    plat_rect = pygame.Rect(p.x, p.y, p.image.get_width(), p.image.get_height())
                    if player.vy >= 0 and player.rect.colliderect(plat_rect):
                        if player.rect.bottom <= plat_rect.top + 40:
                            player.rect.bottom = plat_rect.top
                            player.vy = 0
                            player.is_jumping = [False,False]
                            on_platform_this_frame = True

                if on_platform_this_frame and not scroll_started:
                    scroll_started = True

                if scroll_started:
                    # Augmentation du score quand ça scroll
                    score += 1

                    for p in activePlates:
                        p.update()
                    for e in enemies:
                        e.rect.bottom = e.platform_sprite.y
                    enemies = recycle_platforms_and_enemies(enemies, enemy_img,score)

                for e in enemies:
                    e.mouvement_uniforme_in_platform()
                    # Détection Game Over : Ennemi
                    if player.rect.colliderect(e.rect):
                        print("GAME OVER : Ennemi touché !")
                        if not menu.muted:
                            pygame.mixer.Sound.play(menu.sound_fail)
                        game_over = True
                        break

            screen.blit(utils.getBackground(), (0, 0))


            for p in activePlates:
                p.draw(screen)
            for e in enemies:
                screen.blit(e.image, e.rect.topleft)

            player.draw(screen)

            draw_text(screen, f"Score : {score}", 30, BLACK, WIDTH / 2, 10)

            #Affichage écran Game Over
            if game_over:
                # Fond semi-transparent noir
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(150)
                overlay.fill(BLACK)
                screen.blit(overlay, (0, 0))
                draw_text(screen, "GAME OVER", 80, RED, WIDTH / 2, HEIGHT / 2 - 50)
                draw_text(screen, f"Score Final: {score}", 40, WHITE, WIDTH / 2, HEIGHT / 2 + 20)
                draw_text(screen, "Appuyez sur ENTREE pour rejouer", 25, WHITE, WIDTH / 2, HEIGHT / 2 + 80)
                pygame.mixer_music.stop()
                pygame.mixer.Sound.stop(menu.sound)

            pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()