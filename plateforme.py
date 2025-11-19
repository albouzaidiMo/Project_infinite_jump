import random

import pygame
from os.path import join
from pygame import rect
import utils
import random
import threading

activePlates = []
rects = [(200,80), (150, 80), (250, 80)]
xx = [600, 300, 0]
y_change = 1.7

class Plateform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(join("assets","plateforme.png"))
        self.image = pygame.transform.scale(self.image, rects[random.randint(0, len(rects) - 1)])
        self.x = 600 -  xx[random.randint(0,2)]
        self.y = 300
        self.enemy = None

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def getrect(self):
        return self.image.get_rect()

    def update(self):
        self.y += y_change

    def draw(self, screen):
        #screen.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(screen, pygame.Color('black'), [self.x, self.y,  self.image.get_width(), self.image.get_height()], 0)
        #pygame.display.flip()
        screen.blit(self.image, (self.x, self.y))


def spawnPlateform():
    plt = Plateform()
    activePlates.append(plt)
    return plt