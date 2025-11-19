import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 540
        self.vx = 0
        self.vy = 0
        self.gravity = 1
        self.is_jumping = [False,False]
        self.width = self.rect.width
        self.height = self.rect.height
        self.player_y_change = 50
        self.player_x_change = 5
    def jump(self):
        if not self.is_jumping[0]:
            self.vy = -20
            self.is_jumping[0] = True
        elif not self.is_jumping[1]:
            self.vy = -15
            self.is_jumping[1] = True


    def update(self, screen_height):
        self.rect.y += self.vy
        self.vy += self.gravity

        if self.rect.y + self.height >= screen_height:
            self.rect.y = screen_height- self.height
            self.vy = 0
            self.is_jumping = [False,False]
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def left(self):
        self.rect.x -= self.player_x_change

    def right(self):
        self.rect.x += self.player_x_change

    def frontiere(self):
        if self.rect.left > 800:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = 800