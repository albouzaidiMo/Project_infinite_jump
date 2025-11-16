import pygame
from player import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
screen1=pygame.image.load('rectangle.png')
player = Player(screen1)
player_x = player.x
player_y = player.y
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.left()
    if keys[pygame.K_RIGHT]:
        player.right()
    if keys[pygame.K_SPACE]:
        player.jump()

    player.update(580)
    screen.fill((0, 0, 0))
    player.draw(screen)
    clock.tick(60)
    pygame.display.update()
pygame.quit()
