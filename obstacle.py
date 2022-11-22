import pygame, os

class Obstacle:
    def __init__(self, screen_width, screen_height):
        # cactus values
        self.cactus_width = round(screen_width/18)
        self.cactus_height = round(screen_height/4)
        self.cactus_y = round(screen_height/1.75)
        self.set_cactus_surface()

        # bird values
        self.bird_width = round(screen_width/18)
        self.bird_height = round(screen_height/10)
        self.set_bird_surface()

    def create_cactus(self, x):
        new_cactus = Cactus(self.cactus_surface, x, self.cactus_y)
        return new_cactus

    def create_bird(self, x, y):
        new_bird = Bird(self.bird_surface, x, y)
        return new_bird

    def set_cactus_surface(self):
        path = os.path.join('assets/images/cactus.png')
        image = pygame.image.load(path).convert_alpha()
        self.cactus_surface = pygame.transform.scale(image, (self.cactus_width, self.cactus_height))

    def set_bird_surface(self):
        path = os.path.join('assets/images/bird.png')
        image = pygame.image.load(path).convert_alpha()
        self.bird_surface = pygame.transform.scale(image, (self.bird_width, self.bird_height))

class Cactus:
    def __init__(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y
        self.set_rect()
    
    def update(self, dx):
        self.x += dx
        self.rect.x = self.x

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def set_rect(self):
        self.rect = pygame.Rect(
            self.x, self.y, self.surface.get_width(), self.surface.get_height())

class Bird:
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.surface = surface
        self.set_rect()
    
    def update(self, dx):
        self.x += dx
        self.rect.x = self.x

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())