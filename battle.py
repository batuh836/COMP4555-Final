import pygame, os
from enemy import *

class Battle:
    def __init__(self, screen_width, screen_height):
        self.width = round(screen_width*0.9)
        self.height = round(screen_height*0.75)
        self.x = screen_width/2 - self.width/2
        self.y = screen_height/2 - self.height/2

        # surface sizes
        self.target_size = (50, 50)

        # enemy positions
        self.enemy_pos_left = (self.width/2, self.height/2)
        self.enemy_pos_center = (self.width/1.5, self.height/2)
        self.enemy_pos_right = (self.width/1.25, self.height/2)
        self.enemy_pos_top = (self.width/1.5, self.height/3.5)
        self.enemy_pos_bottom = (self.width/1.5, self.height/1.5)

        # target positions
        self.enemy_pos = self.enemy_pos_center
        self.player_target_pos = self.enemy_pos_center

        self.bat = Enemy()
        self.set_surfaces()
        self.set_rect()
        self.set_sound()

    def start(self, screen):
        self.show(screen)

    def show(self, screen):
        screen.blit(self.bg, (self.x, self.y))
        screen.blit(self.bat, self.enemy_pos)
        screen.blit(self.target, self.player_target_pos)

    def set_surfaces(self):
        bg_path = os.path.join('assets/images/battle_bg.png')
        target_path = os.path.join('assets/images/target.png')

        bg_image = pygame.image.load(bg_path).convert_alpha()
        target_image = pygame.image.load(target_path).convert_alpha()

        self.bg = pygame.transform.scale(bg_image, (self.width, self.height))
        self.target = pygame.transform.scale(target_image, self.target_size)

    def set_rect(self):
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def fire(self):
        if self.player_target_pos == self.enemy_pos:
            # enemy takes damage
            # hit sound plays
            # animation??
            pass
        else:
            # miss sound plays
            pass

    def set_target(self, keys=[]):
        if keys[pygame.K_UP]:
            self.player_target_pos = self.enemy_pos_top
        elif keys[pygame.K_DOWN]:
            self.player_target_pos = self.enemy_pos_bottom
        elif keys[pygame.K_LEFT]:
            self.player_target_pos = self.enemy_pos_left
        elif keys[pygame.K_RIGHT]:
            self.player_target_pos = self.enemy_pos_right
        else:
            self.player_target_pos = self.enemy_pos_center

    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)

    def battle_controls(self, keys):
        self.set_target(keys)
        if keys[pygame.K_SPACE]:
            self.fire()