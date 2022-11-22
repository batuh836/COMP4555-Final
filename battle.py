import pygame, os

class Battle:
    def __init__(self, screen_width, screen_height):
        self.width = round(screen_width*0.9)
        self.height = round(screen_height*0.75)
        self.x = screen_width/2 - self.width/2
        self.y = screen_height/2 - self.height/2
        self.set_surface()
        self.set_rect()
        self.set_sound()

    def start(self, screen):
        self.show(screen)

    def update(self):
        self.set_surface()

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def set_surface(self):
        path = os.path.join('assets/images/battle_bg.png')
        image = pygame.image.load(path).convert_alpha()
        self.surface = pygame.transform.scale(image, (self.width, self.height))

    def set_rect(self):
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)