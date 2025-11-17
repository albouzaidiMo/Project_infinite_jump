import pygame
import random

def random_position_in_platform_with_width( platform , height , width):  # platform = [x_min, x_max, y_plat]
    x_min = platform [0]
    x_max = platform [1]
    y_plat = platform [2]
    x_random = random.randint( x_min , x_max - width)
    return x_random , y_plat + height

class Enemy (pygame.sprite.Sprite):
    
    def __init__(self,image,platform):  # platform =[ x_min, x_max, y_plat] les paramètres de la platformes
        
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.platform = platform

        self.width = 10          # largeur de l'ennemi
        self.height = 10         # hauteur de l'ennemi
        
        position = random_position_in_platform_with_width(self.platform, self.height , self.width)
        self.rect.x = position [0]
        self.rect.y = position [1]
        
        self.x_change = 5    # déplacement de l'ennemi
        
        self.is_mvt_left = False  # la direction du mouvement à l'état initial

