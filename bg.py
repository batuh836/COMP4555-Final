import os, pygame

class BG:
    def __init__(self, settings, x, screen):
        self.settings = settings
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.x = x
        self.set_surface()

    def update(self, dx):
        self.x += dx/2
        if self.x <= -self.width:
            self.x = self.width

    def show(self, screen):
        screen.blit(self.surface, (self.x, 0))

    def set_surface(self):
        path = self.settings.get_level_setting("bg")
        self.surface = pygame.image.load(path).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (self.width, self.height))

class FG:
    def __init__(self, settings, x, screen):
        self.settings = settings
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.x = x
        self.set_surface()

    def update(self, dx):
        self.x += dx
        if self.x <= -self.width:
            self.x = self.width

    def show(self, screen):
        screen.blit(self.surface, (self.x, 0))

    def set_surface(self):
        path = self.settings.get_level_setting("fg")
        self.surface = pygame.image.load(path).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (self.width, self.height))