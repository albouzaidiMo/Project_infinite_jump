import pygame
from os.path import join

#def getBackground():
    #img = pygame.image.load(join("assets","floor.png"))
    #img = pygame.transform.scale(img, (800, 600))
    #return img

def getMenuImg():
    image = pygame.image.load(join("assets","menu.jpg"))
    image = pygame.transform.scale(image, (800, 600))
    return image