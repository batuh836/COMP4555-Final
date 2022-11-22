import pygame, os

class Obstacle:
    def __init__(self):
        # cactus values
        self.cactus_width = 34
        self.cactus_height = 44
        self.cactus_y = 80
        self.set_cactus_texture()

        # bird values
        self.bird_width = 34
        self.bird_height = 24
        self.set_bird_texture()

    def create_cactus(self, x):
        new_cactus = Cactus(self.cactus_texture, x, self.cactus_y)
        return new_cactus

    def create_bird(self, x, y):
        new_bird = Bird(self.bird_texture, x, y)
        return new_bird

    def set_cactus_texture(self):
        path = os.path.join('assets/images/cactus.png')
        self.cactus_texture = pygame.image.load(path).convert_alpha()
        self.cactus_texture = pygame.transform.scale(
            self.cactus_texture, (self.cactus_width, self.cactus_height))

    def set_bird_texture(self):
        path = os.path.join('assets/images/bird.png')
        self.bird_texture = pygame.image.load(path).convert_alpha()
        self.bird_texture = pygame.transform.scale(
            self.bird_texture, (self.bird_width, self.bird_height))

class Cactus:
    def __init__(self, texture, x, y):
        self.texture = texture
        self.x = x
        self.y = y
        self.set_rect()
    
    def update(self, dx):
        self.x += dx
        self.rect.x = self.x

    def show(self, screen):
        screen.blit(self.texture, (self.x, self.y))

    def set_rect(self):
        self.rect = pygame.Rect(
            self.x, self.y, self.texture.get_width(), self.texture.get_height())

class Bird:
    def __init__(self, texture, x, y):
        self.x = x
        self.y = y
        self.texture = texture
        self.set_rect()
    
    def update(self, dx):
        self.x += dx
        self.rect.x = self.x

    def show(self, screen):
        screen.blit(self.texture, (self.x, self.y))

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.texture.get_width(), self.texture.get_height())