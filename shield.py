import pygame
import random
from os.path import join


class Shield:
    def __init__(self, platform):
        self.image = pygame.image.load(join("assets", "bouclier.png"))
        self.image = pygame.transform.scale(self.image, (30, 30))

        self.platform = platform
        self.rect = self.image.get_rect()
        self.offset_x = platform.image.get_width() // 2 - 15
        self.offset_y = -35
        self.rect.x = platform.x + self.offset_x
        self.rect.y = platform.y + self.offset_y
        self.collected = False

        self.float_offset = 0
        self.float_speed = 0.1
#le bouclier suit la plateforme
    def update(self):
        if not self.collected:
            self.rect.x = self.platform.x + self.offset_x
            self.rect.y = self.platform.y + self.offset_y

            self.float_offset += self.float_speed
            if int(self.float_offset) % 20 < 10:
                self.rect.y -= 5
            else:
                self.rect.y += 5

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect.topleft)

#Gestion de l'apparition du bouclier
class ShieldManager:
    def __init__(self):
        self.shield = None
        self.spawn_interval = 800
        self.last_spawn_score = 0
        self.shield_sound = pygame.mixer.Sound(join("assets", "shield.mp3"))
        self.shield_sound.set_volume(0.5)
    def spawn_shield(self, platforms, current_score):
        if self.shield is None and current_score - self.last_spawn_score >= self.spawn_interval:
            visible_platforms = [p for p in platforms if 0< p.y < 200]
            if visible_platforms:
                platform = random.choice(visible_platforms)
                self.shield = Shield(platform)
                self.last_spawn_score = current_score

    def update(self, platforms, current_score):
        if self.shield is not None:
            if not self.shield.collected:
                self.shield.update()

            if self.shield.rect.y > 700 or self.shield.collected:
                self.shield = None

        self.spawn_shield(platforms, current_score)

    def check_collision(self, player, is_muted=False):
        if self.shield is not None and not self.shield.collected:
            if player.rect.colliderect(self.shield.rect):
                self.shield.collected = True
                
                if self.shield_sound and not is_muted:
                    self.shield_sound.play()
                return True
        return False

    def draw(self, screen):
        if self.shield is not None:
            self.shield.draw(screen)

#Affichage de l'état de protection
def draw_shield_indicator(screen, x, y):
    shield_icon = pygame.image.load(join("assets", "bouclier.png"))
    shield_icon = pygame.transform.scale(shield_icon, (25, 25))
    screen.blit(shield_icon, (x, y))

    font = pygame.font.SysFont("arial", 20)
    text = font.render("PROTEGE", True, (0, 200, 255))
    screen.blit(text, (x + 30, y + 2))