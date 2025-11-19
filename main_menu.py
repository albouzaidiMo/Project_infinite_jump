import pygame
from os.path import join



class MainMenu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.muted = False
        self.started = False
        self.sound = pygame.mixer.Sound(join("assets", "music.wav"))
        self.sound_fail= pygame.mixer.Sound(join("assets", "fail_music.wav"))

        pygame.mixer.Sound.play(self.sound)


    def get_menuImg(self):
        image = pygame.image.load(join("assets","menu.jpg"))
        image = pygame.transform.scale(image, (800, 600))
        return image

    def get_startRect(self):
        return pygame.Rect(215, 215, 375, 87)

    def get_endRect(self):
        return pygame.Rect(208, 342, 383, 87)

    def get_muteRect(self):
        return pygame.Rect(650, 409, 99, 66)

    def run(self, screen):
        if self.muted:
            pygame.draw.line(screen, 'red', (649, 408), (751, 475), 5)
            pygame.display.flip()
        if not self.started:
            screen.blit(self.get_menuImg(), self.get_menuImg().get_rect())
            pygame.display.flip()
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if self.get_startRect().collidepoint(pos):
                        print(pos)
                        print("WE PLAYYY")
                        self.started = True
                        return 1
                    elif self.get_endRect().collidepoint(pos):
                        print("WE STOPPP")
                        return 0
                    elif self.get_muteRect().collidepoint(pos):
                        self.muted = not self.muted
                        if self.muted:
                            pygame.mixer_music.stop()
                            pygame.mixer.Sound.stop(self.sound)
                        else:
                            pygame.mixer.Sound.play(self.sound)

                        return 2
                if event.type == pygame.QUIT:
                    return 0

        return 2

