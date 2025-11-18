import pygame
import random


def random_position_in_platform_with_width(platform, height, width):  # platform = [x_min, x_max, y_plat]
    x_min = platform[0]
    x_max = platform[1]
    y_plat = platform[2]
    x_random = random.randint(x_min, x_max - width)
    return x_random, y_plat + height


class Enemy(pygame.sprite.Sprite):

    def __init__(self, image, platform):  # platform =[ x_min, x_max, y_plat] les paramètres de la platformes

        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.platform = platform

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
        x_min = self.platform[0]
        x_max = self.platform[1]
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
