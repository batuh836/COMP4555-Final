import pygame, os, random

class Shot:
    def __init__(self, settings):
        self.settings = settings
        self.width = 75
        self.height = 75
        self.shot_speed = 7.5
        self.player_shot = []
        self.enemy_shot = []
        self.set_surfaces()

    def get_shot(self, type, x, y):
        if type == "player":
            speed = self.shot_speed
            frames = self.player_shot
        elif type == "enemy":
            speed = -self.shot_speed
            frames = self.enemy_shot
        return ShotEffect(frames, speed, x, y)

    def set_surfaces(self):
        player_shot_path = self.settings.get_vfx_setting("player_shot")
        enemy_shot_path = self.settings.get_vfx_setting("enemy_shot")
        for i in range(11):
            player_path = os.path.join(player_shot_path, f'shot_{i}.png')
            enemy_path = os.path.join(enemy_shot_path, f'shot_{i}.png')
            player_image = pygame.image.load(player_path).convert_alpha()
            enemy_image = pygame.image.load(enemy_path).convert_alpha()
            self.player_shot.append(pygame.transform.scale(player_image, (self.width, self.height)))
            self.enemy_shot.append(pygame.transform.scale(enemy_image, (self.width, self.height)))

class ShotEffect:
    def __init__(self, frames, speed, x, y):
        self.width = 75
        self.height = 75
        self.x = x
        self.y = y
        self.speed = speed
        self.frame_num = 0
        self.frames = frames
        self.surface = frames[0]
        self.set_rect()

    def update(self, loop):
        # move shot
        self.x += self.speed
        self.rect.x = self.x

        # update surface
        if loop % 3 == 0:
            self.frame_num = (self.frame_num + 1) % 11
            self.surface = self.frames[self.frame_num]

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))
        
    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)