import pygame
from enemies import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
screen1 = pygame.image.load("enemytest.png")
platform_sol = [ 0 , 800 , 600]
enemy = Enemy(screen1, platform_sol)
enemy_x = enemy.rect.x
enemy_y = enemy.rect.y
running = True
print ( enemy.rect.x,enemy.rect.y, enemy.height, enemy.width)
while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    enemy.mouvement_uniforme_in_platform()
    screen.fill((0, 0, 0))
    enemy.draw(screen)
    clock.tick(60)
    pygame.display.update()
pygame.quit()
