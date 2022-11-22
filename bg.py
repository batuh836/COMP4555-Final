import os, pygame

class BG:
    def __init__(self, x, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.set_texture()

    def update(self, dx):
        self.x += dx
        if self.x <= -self.width:
            self.x = self.height

    def show(self, screen):
        screen.blit(self.texture, (self.x, 0))

    def set_texture(self):
        path = os.path.join('assets/images/bg.png')
        self.texture = pygame.image.load(path).convert()
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))