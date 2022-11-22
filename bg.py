import os, pygame

class BG:
    def __init__(self, x, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.set_surface()

    def update(self, dx):
        self.x += dx
        if self.x <= -self.width:
            self.x = self.width

    def show(self, screen):
        screen.blit(self.surface, (self.x, 0))

    def set_surface(self):
        path = os.path.join('assets/images/bg.png')
        self.surface = pygame.image.load(path).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (self.width, self.height))