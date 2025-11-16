class Player:
    def __init__(self, image):
        self.image = image
        self.x = 580
        self.y = 370
        self.width = 10
        self.height = 10
        self.player_y_change = 50
        self.player_x_change = 5
        self.vy = 0
        self.gravity = 1
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.vy = -15
            self.is_jumping = True


    def update(self, screen_height):
        self.y += self.vy
        self.vy += self.gravity

        if self.y + self.height >= screen_height:
            self.y = screen_height- self.height
            self.vy = 0
            self.is_jumping = False
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def left(self):
        self.x -= self.player_x_change

    def right(self):
        self.x += self.player_x_change


