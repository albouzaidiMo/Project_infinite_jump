import pygame
import sys
import time


import plateforme as pf

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Spawn some platforms
platforms = []
for _ in range(3):
    platforms.append(pf.spawnPlateform())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background
    screen.fill((30, 30, 30))

    # Update + draw platforms
    for p in platforms:
        p.update()
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
