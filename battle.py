import pygame, os

class Battle:
    def __init__(self, width, height):
        self.width = width*0.75
        self.height = height*0.75
        self.set_texture()
        self.set_rect()
        self.set_sound()

    def start(self, screen):
        self.show(screen)

    def update(self, loop):
        self.set_texture()

    def show(self, screen):
        screen.blit(self.texture, (0,0))

    def set_texture(self):
        path = os.path.join(f'assets/images/battle_bg.png')
        self.texture = pygame.image.load(path).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def set_rect(self):
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)