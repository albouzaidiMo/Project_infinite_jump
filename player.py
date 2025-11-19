import pygame
from os.path import join
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.images_right = [pygame.image.load(join("assets", "mario_droit1.png")),pygame.image.load(join("assets", "mario_saut1.png"))]
        self.images_left = [pygame.transform.flip(i, True, False) for i in self.images_right]
        self.images_right = [pygame.transform.scale(i, (21, 36)) for i in self.images_right]
        self.images_left = [pygame.transform.scale(i, (21, 36)) for i in self.images_left]
        self.img_act = image
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
        self.frame = 0
        self.animation = 0.15
        self.direction = "right"
    def animate(self, moving1):
        if not moving1:
            self.img_act = self.image
            return

        self.frame += self.animation
        if self.frame >= len(self.images_right):
            self.frame = 0

        if self.direction == "right":
            self.img_act = self.images_right[int(self.frame)]
        else:
            self.img_act = self.images_left[int(self.frame)]
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
        screen.blit(self.img_act, self.rect.topleft)

    def left(self):
        self.rect.x -= self.player_x_change
        self.direction = "left"

    def right(self):
        self.rect.x += self.player_x_change
        self.direction = "right"

    def frontiere(self):
        if self.rect.left > 800:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = 800