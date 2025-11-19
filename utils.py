import pygame
from os.path import join

def getBackground():
    img = pygame.image.load(join("assets","background.jpg"))
    img = pygame.transform.scale(img, (800, 600))
    return img

def getMenuImg():
    image = pygame.image.load(join("assets","menu.jpg"))
    image = pygame.transform.scale(image, (800, 600))
    return image

def getPlayerImg():
    image = pygame.image.load(join("assets","player.jpg"))
    image = pygame.transform.scale(image, (10, 20))
    return image

def getEnemiesImg():
    image = pygame.image.load(join("assets","enemies.jpg"))
    image = pygame.transform.scale(image, (10, 10))
    return image