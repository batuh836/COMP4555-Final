import pygame, random

class Enemy:
    def __init__(self, settings):
        self.settings = settings
        self.health = self.settings.get_level_setting("enemy_health")
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.color = (255, 255, 255)
        self.set_surface()

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

        label = self.font.render(f"{health_bar} HP", 1, self.color)
        location = (screen.get_width() * 0.9 - label.get_width(), screen.get_height() * 0.25)
        screen.blit(label, location)

    def set_surface(self):
        path = self.settings.get_level_setting("enemy")
        image = pygame.image.load(path).convert_alpha()
        self.size = (60, 60)
        self.surface = pygame.transform.scale(image, self.size)

class Boss:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.ground_height = screen.get_height()*0.65
        self.name = self.settings.get_level_setting("boss_name")
        self.health = self.settings.get_level_setting("boss_health")
        self.strength = self.settings.get_level_setting("boss_strength")
        self.dx = self.settings.get_level_setting("boss_speed")
        self.dy = 1
        self.is_hit = False
        self.knock_back_time = 0
        self.knock_back_duration = 10
        self.shot_timer = 0
        self.shot_time = self.settings.get_level_setting("boss_shot_time")
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.color = (255, 255, 255)
        self.set_surface()
        self.set_rect()

    def is_alive(self):
        return self.health > 0

    def knockback(self):
        self.knock_back_time = 0
        self.is_hit = True

    def shoot(self, game):
        self.shot_timer = 0
        y = random.choice([self.ground_height, self.ground_height*0.25])
        game.enemy_shots.append(game.shot.get_shot("enemy", self.rect.centerx, y))
        game.effects.play_sfx("enemy_shoot") 

    def update(self, game):
        if self.is_alive():
            if self.surface.get_alpha() < 255:
                # enemy appears
                self.surface.set_alpha(self.surface.get_alpha() + 1)
            else:
                # enemy shot
                self.shot_timer += 1
                if self.shot_timer >= self.shot_time:
                    self.shoot()
                
                # enemy movement
                if game.loop % 6 == 0:
                    if self.is_hit:
                        self.knock_back_time += 1
                        self.x += self.dx
                        if self.knock_back_time >= self.knock_back_duration:
                            self.is_hit = False
                    else:
                        self.x -= self.dx
                        self.y += self.dy
                        self.rect.x = self.x
                        self.rect.y = self.y

                        if self.rect.top <= 0:
                            self.dy = 1
                        elif self.rect.bottom >= self.screen_height:
                            self.dy = -1

        else:
            self.surface.set_alpha(self.surface.get_alpha() - 1)

            if self.surface.get_alpha() > 0 and game.loop % 20 == 0:
                effect_location = random.choice([
                    self.rect.center,
                    self.rect.topleft,
                    self.rect.topright,
                    self.rect.bottomleft,
                    self.rect.bottomright
                ])
                game.vfxs.append(game.effects.create_vfx("hit", effect_location))
                game.effects.play_sfx("enemy_hit") 

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))
        if self.is_alive():
            self.show_health(screen)
    
    def show_health(self, screen):
        health_bar = ""
        for _ in range(self.health):
            health_bar += "|"

        label = self.font.render(f"{health_bar} {self.name}", 1, self.color)
        location = (screen.get_width() - label.get_width() - 10, 10)
        screen.blit(label, location)

    def set_surface(self):
        path = self.settings.get_level_setting("boss")
        image = pygame.image.load(path).convert_alpha()
        self.surface = pygame.transform.scale2x(image)
        self.surface.set_alpha(0)
        self.size = self.surface.get_size()
        self.x = self.screen_width - self.surface.get_width() - 10
        self.y = 10

    def set_rect(self):
        self.rect = pygame.Rect((self.x, self.y), (self.size))