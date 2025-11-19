import pygame
import random
from os.path import join
from constants import * # Import depuis constants.py au lieu de Jeu.py

def random_position_in_platform_with_width(platform_data, height, width):
    # platform_data est une liste : [x_min, x_max, y_plat]
    x_min = platform_data[0]
    x_max = platform_data[1]
    y_plat = platform_data[2]
    # Sécurité : s'assurer qu'il y a de la place pour l'ennemi
    if x_max - width > x_min:
        x_random = random.randint(x_min, x_max - width)
    else:
        x_random = x_min
        
    return x_random, y_plat # L'ennemi est posé SUR la plateforme (y_plat est le haut)

class Enemy(pygame.sprite.Sprite):
    # J'ai inversé les arguments pour correspondre à l'appel fait dans Jeu.py : Enemy(image, params)
    def __init__(self, image, platform_data): 
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        
        # platform_data = [x_min, x_max, y]
        self.platform_data = platform_data 
        
        # On initialise la référence au sprite plateforme à None (sera rempli par Jeu.py)
        self.platform_sprite = None 

        self.width = self.image.get_width()   # Utiliser la vraie largeur de l'image
        self.height = self.image.get_height() # Utiliser la vraie hauteur de l'image

        position = random_position_in_platform_with_width(self.platform_data, self.height, self.width)
        self.rect.x = position[0]
        self.rect.bottom = platform_data[2]   # On place le bas de l'ennemi sur le haut de la plateforme

        self.x_change = 2  # Vitesse de déplacement (5 était très rapide)
        self.is_mvt_left = False # Direction initiale

    def mvt_left_update(self):
        self.rect.x -= self.x_change

    def mvt_right_update(self):
        self.rect.x += self.x_change

    def is_possible_left_right(self):
        # On utilise les données de la liste [x_min, x_max, y]
        x_min = self.platform_data[0]
        x_max = self.platform_data[1]
        
        is_possible = [True, True]

        # Si l'ennemi va trop à gauche
        if self.rect.x - self.x_change < x_min:
            is_possible[0] = False

        # Si l'ennemi va trop à droite
        if self.rect.right + self.x_change > x_max:
            is_possible[1] = False

        return is_possible

    def mouvement_uniforme_in_platform(self):
        # Met à jour les limites au cas où la plateforme a bougé (scrolling)
        if self.platform_sprite:
            x_min = self.platform_sprite.x
            x_max = self.platform_sprite.x + self.platform_sprite.image.get_width()
            self.platform_data = [x_min, x_max, self.platform_sprite.y]

        is_possible = self.is_possible_left_right()

        if self.is_mvt_left: # Déplacement vers la gauche
            if is_possible[0]:
                self.mvt_left_update()
            else:
                self.is_mvt_left = False # On change de direction -> Droite

        else: # Déplacement vers la droite
            if is_possible[1]:
                self.mvt_right_update()
            else:
                self.is_mvt_left = True # On change de direction -> Gauche