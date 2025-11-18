import pygame
import random
from os.path import join

import Jeu
#import HEIGHT, plateforme_par_ligne, WIDTH, GAP_Y
from plateforme import activePlates, spawnPlateform


def random_position_in_platform_with_width(platform, height, width):  # platform = [x_min, x_max, y_plat]
    x_min = platform.x
    x_max = platform.x + platform.get_width()
    y_plat = platform.y
    x_random = random.randint(x_min, x_max - width)
    return x_random, y_plat + height


class Enemy(pygame.sprite.Sprite):

    def __init__(self, platform, image = pygame.transform.scale(pygame.image.load(join("assets", "rectangle.png")), (20, 20))):  # platform =[ x_min, x_max, y_plat] les paramètres de la platformes

        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.platform = platform
        platform.enemy = self

        self.width = 10  # largeur de l'ennemi
        self.height = 10  # hauteur de l'ennemi

        position = random_position_in_platform_with_width(self.platform, self.height, self.width)
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.x_change = 5  # déplacement de l'ennemi

        self.is_mvt_left = False  # la direction du mouvement à l'état initial

    def mvt_left_update(self):
        self.rect.x -= self.x_change

    def mvt_right_update(self):
        self.rect.x += self.x_change

    def is_possible_left_right(self):  # return une liste de Boolien
        x_min = self.platform.x
        x_max = self.platform.x + self.platform.get_width()
        is_possible = [True, True]

        if self.rect.x - self.x_change < x_min:  # si l'ennemi va sortir de la platforme en se déplaçant vers la gauche
            is_possible[0] = False

        if self.rect.x + self.x_change + self.width > x_max:  # si l'ennemi va sortir de la platforme en se déplaçant vers la droite
            is_possible[1] = False

        return is_possible  # is_possible[0] mvt en gauche , is_possible[1] mvt en droite

    def mouvement_uniforme_in_platform(self):
        is_possible = self.is_possible_left_right()

        if self.is_mvt_left:  # si déplacement est vers la gauche
            if is_possible[0]:
                self.mvt_left_update()
            else:
                self.is_mvt_left = False

        else:  # si le déplacement est vers la droite
            if is_possible[1]:
                self.mvt_right_update()
            else:
                self.is_mvt_left = True

    def spawn(self):
        x_min = self.platform.x
        x_max = self.platform.x + self.platform.image.get_width()
        platform_params = [x_min, x_max, self.platform.y]
        enemy = Enemy(self.platform)
        enemy.rect.bottom = self.platform.y
        enemy.platform_sprite = self.platform
        self.platform.enemy = enemy
        return enemy

def init_platforms_and_enemies():
    activePlates.clear()
    enemies = []
    y = Jeu.HEIGHT - 80
    while y > -Jeu.HEIGHT:
        for i in range(Jeu.plateforme_par_ligne):
            p = spawnPlateform()
            p.y = y
            p.x = random.randint(0, Jeu.WIDTH - p.image.get_width())
            if random.random() < 0.4:
                e = Enemy(p)
                enemies.append(e)
            else:
                p.enemy = None
        y -= Jeu.GAP_Y
    return enemies