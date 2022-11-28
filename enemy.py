import pygame, os, math

class Enemy:
    def __init__(self):
        self.size = (40, 30)
        self.health = 3
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.color = (255, 255, 255)
        self.set_surface()
        self.set_rect()
        self.set_sound()

    def is_alive(self):
        return self.health > 0

    def update(self):
        pass

    def show(self, screen, pos):
        screen.blit(self.surface, pos)

    def show_health(self, screen):
        health_bar = ""
        for _ in range(self.health):
            health_bar += "|"

        label = self.font.render(f"{health_bar} BAT", 1, self.color)
        location = (screen.get_width() * 0.9 - label.get_width(), screen.get_height() * 0.25)
        screen.blit(label, location)

    def set_surface(self):
        bat_path = os.path.join('assets/images/bat.png')
        bat_image = pygame.image.load(bat_path).convert_alpha()
        self.surface = pygame.transform.scale(bat_image, self.size)

    def set_rect(self):
        pass

    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)