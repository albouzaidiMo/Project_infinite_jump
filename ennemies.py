import pygame
import random
def random_position_in_platform_with_width(platform_data, height, width):

    x_min = platform_data[0]
    x_max = platform_data[1]
    y_plat = platform_data[2]

    if x_max - width > x_min:
        x_random = random.randint(x_min, x_max - width)
    else:
        x_random = x_min
        
    return x_random, y_plat

class Enemy(pygame.sprite.Sprite):

    def __init__(self, image, platform_data): 
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        

        self.platform_data = platform_data 
        

        self.platform_sprite = None 

        self.width = self.image.get_width()   
        self.height = self.image.get_height() 

        position = random_position_in_platform_with_width(self.platform_data, self.height, self.width)
        self.rect.x = position[0]
        self.rect.bottom = platform_data[2]   

        self.x_change = 2  
        self.is_mvt_left = False 

    def mvt_left_update(self):
        self.rect.x -= self.x_change

    def mvt_right_update(self):
        self.rect.x += self.x_change

    def is_possible_left_right(self):

        x_min = self.platform_data[0]
        x_max = self.platform_data[1]
        
        is_possible = [True, True]


        if self.rect.x - self.x_change < x_min:
            is_possible[0] = False


        if self.rect.right + self.x_change > x_max:
            is_possible[1] = False

        return is_possible

    def mouvement_uniforme_in_platform(self):

        if self.platform_sprite:
            x_min = self.platform_sprite.x
            x_max = self.platform_sprite.x + self.platform_sprite.image.get_width()
            self.platform_data = [x_min, x_max, self.platform_sprite.y]

        is_possible = self.is_possible_left_right()

        if self.is_mvt_left: 
            if is_possible[0]:
                self.mvt_left_update()
            else:
                self.is_mvt_left = False 
        else: 
            if is_possible[1]:
                self.mvt_right_update()
            else:
                self.is_mvt_left = True 