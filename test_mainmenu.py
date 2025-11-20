import pygame
import sys
import time

import main_menu as menu

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

main_menu = menu.MainMenu()

running = True
while running:

    result = main_menu.run(screen)
    if result == 1:
        print("Game Started!")
        time.sleep(1)
        running = False   # remove this if you want the game to continue
    elif result == 0:
        print("Quit requested")
        running = False
    elif result == 2:
        pass
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
