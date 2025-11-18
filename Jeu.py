import pygame
import random
from os.path import join
from player import Player
from plateforme import spawnPlateform, activePlates
from ennemies import Enemy
import utils
#csts
WIDTH, HEIGHT = 800, 600
GAP_Y = 170
plateforme_par_ligne = 1

def create_enemy_on_platform(plateform, enemy_img):
    x_min = plateform.x
    x_max = plateform.x + plateform.image.get_width()
    platform_params = [x_min, x_max, plateform.y]
    enemy = Enemy(enemy_img, platform_params)
    enemy.rect.bottom = plateform.y
    enemy.platform_sprite = plateform
    plateform.enemy = enemy
    return enemy


def init_platforms_and_enemies(enemy_img):
    activePlates.clear()
    enemies = []
    y = HEIGHT - 80
    while y > -HEIGHT:
        for _ in range(plateforme_par_ligne):
            p = spawnPlateform()
            p.y = y
            p.x = random.randint(0, WIDTH - p.image.get_width())
            if random.random() < 0.4:
                e = create_enemy_on_platform(p, enemy_img)
                enemies.append(e)
            else:
                p.enemy = None
        y -= GAP_Y
    return enemies
def recycle_platforms_and_enemies(enemies, enemy_img):
    min_y = min(p.y for p in activePlates)
    for p in activePlates:
        if p.y > HEIGHT + 50:
            p.y = min_y - GAP_Y
            p.x = random.randint(0, WIDTH - p.image.get_width())
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
                if random.random() < 0.4:
                    e = create_enemy_on_platform(p, enemy_img)
                    enemies.append(e)
    return enemies


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario vertical")
    clock = pygame.time.Clock()
    #background = utils.getBackground()
    player_img = pygame.image.load(join("assets", "rectangle.png")).convert_alpha()
    enemy_img = pygame.transform.scale(player_img, (20, 20))
    player = Player(player_img)
    enemies = init_platforms_and_enemies(enemy_img)

    running = True
    scroll_started = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    player.jump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.left()
        if keys[pygame.K_RIGHT]:
            player.right()
        player.frontiere()
        player.update(HEIGHT)
        if scroll_started and player.rect.bottom >= HEIGHT:
            print("GAME OVER : Tu es tombé !")
            running = False
        on_platform_this_frame = False
        for p in activePlates:
            plat_rect = pygame.Rect(p.x, p.y, p.image.get_width(), p.image.get_height())
            if player.vy >= 0 and player.rect.colliderect(plat_rect):
                if player.rect.bottom <= plat_rect.top + 15:
                    player.rect.bottom = plat_rect.top
                    player.vy = 0
                    player.is_jumping = False
                    on_platform_this_frame = True
        if on_platform_this_frame and not scroll_started:
            scroll_started = True
        if scroll_started:
            for p in activePlates:
                p.update()
            for e in enemies:
                e.rect.bottom = e.platform_sprite.y
            enemies = recycle_platforms_and_enemies(enemies, enemy_img)

        '''for e in enemies:
            e.mouvement_uniforme_in_platform()
            if player.rect.colliderect(e.rect):
                print("GAME OVER : Ennemi touché !")
                running = False
                break'''
        #screen.blit(background, (0, 0))
        screen.fill("white")
        for p in activePlates:
            p.draw(screen)
        for e in enemies:
            screen.blit(e.image, e.rect.topleft)

        player.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
if __name__ == "__main__":
    main()