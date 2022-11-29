import pygame, os, random

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

class Boss:
    def __init__(self, screen_width, screen_height):
        self.size = (screen_width*0.35, screen_height*0.5)
        self.x = screen_width
        self.y = screen_height/2
        self.dx = 1
        self.dy = 1
        self.screen_width = screen_width
        self.ground_height = round(screen_height/1.5)
        self.name = "BOSS"
        self.health = 1
        self.shot_timer = 0
        self.shot_time = 100
        self.can_shoot = False
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.color = (255, 255, 255)
        self.set_surface()
        self.set_rect()
        self.set_sound()

    def is_alive(self):
        return self.health > 0

    def shoot(self, shot):
        self.can_shoot = False
        y = random.choice([self.ground_height, self.ground_height*0.25])
        return shot.get_shot("enemy", self.x, y)

    def update(self, loop):
        if self.is_alive():
            self.shot_timer += 1
            if self.shot_timer >= self.shot_time:
                self.can_shoot = True
                self.shot_timer = 0
            if loop % 6 == 0:
                self.x -= self.dx
                self.y += self.dy
                self.rect.x = self.x
                self.rect.y = self.y

                if self.rect.top <= 0:
                    self.dy = 1
                elif self.rect.bottom >= self.ground_height:
                    self.dy = -1
        else:
            self.surface.set_alpha(self.surface.get_alpha() - 1)

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def show_health(self, screen):
        health_bar = ""
        for _ in range(self.health):
            health_bar += "|"

        label = self.font.render(f"{health_bar} BOSS", 1, self.color)
        location = (screen.get_width() - label.get_width() - 10, 10)
        screen.blit(label, location)

    def set_surface(self):
        bat_path = os.path.join('assets/images/boss_01.png')
        bat_image = pygame.image.load(bat_path).convert_alpha()
        self.surface = pygame.transform.scale(bat_image, self.size)

    def set_rect(self):
        self.rect = pygame.Rect((self.x, self.y), (self.size))

    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)