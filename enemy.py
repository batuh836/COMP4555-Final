import pygame, os, math

class Enemy:
    def __init__(self):
        self.size = (40, 30)
        self.health = 5
        self.set_surface()
        self.set_rect()
        self.set_sound()

    def is_alive(self):
        return self.health > 0

    def update(self):
        pass

    def show(self, screen, pos):
        screen.blit(self.surface, pos)

    def set_surface(self):
        bat_path = os.path.join('assets/images/bat.png')
        bat_image = pygame.image.load(bat_path).convert_alpha()
        self.surface = pygame.transform.scale(bat_image, self.size)

    def set_rect(self):
        pass

    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)