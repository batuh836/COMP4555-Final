import pygame, os, random
from enemy import *

class Battle:
    def __init__(self, game, screen_width, screen_height):
        self.game = game
        self.width = round(screen_width*0.9)
        self.height = round(screen_height*0.75)
        self.x = screen_width*0.5 - self.width*0.5
        self.y = screen_height*0.5 - self.height*0.5

        # surface sizes
        self.target_size = (50, 50)

        # enemy positions
        enemy_pos_center = (self.width*0.65, self.height*0.5)
        enemy_pos_top = (self.width*0.65, self.height*0.2)
        enemy_pos_bottom = (self.width*0.65, self.height*0.8)
        enemy_pos_left = (self.width*0.5, self.height*0.5)
        enemy_pos_right = (self.width*0.8, self.height*0.5)
        self.enemy_positions = [enemy_pos_center, 
                                enemy_pos_top, 
                                enemy_pos_bottom, 
                                enemy_pos_left, 
                                enemy_pos_right]

        # target positions
        self.enemy_current_pos = self.enemy_positions[0]
        self.player_target_pos = self.enemy_positions[0]

        self.set_surfaces()
        self.set_rect()
        self.set_sounds()

    def start(self, screen):
        self.fx_channel.play(self.encounter_sound)
        self.end_battle_timer = 0
        self.player_target_pos = self.enemy_positions[0]
        self.enemy = Enemy()
        self.set_enemy_pos()
        self.show(screen)

    def end(self):
        if self.end_battle_timer == 0:
            self.fx_channel.queue(self.win_sound)
        if self.end_battle_timer == 50:
            self.game.end_battle()
        self.end_battle_timer += 1

    def set_enemy_pos(self):
        random_enemy_pos = random.randint(0, 3)
        new_enemy_positions = self.enemy_positions.copy()
        new_enemy_positions.remove(self.enemy_current_pos)
        self.enemy_current_pos = new_enemy_positions[random_enemy_pos]

    def update(self, loop):
        if loop % 50 == 0:
            self.set_enemy_pos()

    def show(self, screen):
        screen.blit(self.bg, (self.x, self.y))
        if self.enemy.is_alive():
            self.enemy.show_health(screen)
            screen.blit(self.enemy.surface, self.enemy_current_pos)
            screen.blit(self.target, self.player_target_pos)
        else:
            self.end()

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
        self.fx_channel.stop()
        self.fx_channel.play(self.fire_sound)

        if self.player_target_pos == self.enemy_current_pos:
            # graphic
            self.fx_channel.queue(self.hit_sound)
            self.enemy.health -= 1
        else:
            # graphic
            self.fx_channel.queue(self.miss_sound)
            pass

    def set_target(self, keys=[]):
        if keys[pygame.K_UP]:
            self.player_target_pos = self.enemy_positions[1]
        elif keys[pygame.K_DOWN]:
            self.player_target_pos = self.enemy_positions[2]
        elif keys[pygame.K_LEFT]:
            self.player_target_pos = self.enemy_positions[3]
        elif keys[pygame.K_RIGHT]:
            self.player_target_pos = self.enemy_positions[4]
        else:
            self.player_target_pos = self.enemy_positions[0]

    def set_sounds(self):
        # set paths
        encounter_path = os.path.join('assets/sounds/encounter.wav')
        fire_path = os.path.join('assets/sounds/fire.wav')
        hit_path = os.path.join('assets/sounds/hit.wav')
        miss_path = os.path.join('assets/sounds/miss.wav')
        win_path = os.path.join('assets/sounds/win.wav')

        # set sounds
        self.fx_channel = pygame.mixer.Channel(1)
        self.encounter_sound = pygame.mixer.Sound(encounter_path)
        self.fire_sound = pygame.mixer.Sound(fire_path)
        self.hit_sound = pygame.mixer.Sound(hit_path)
        self.miss_sound = pygame.mixer.Sound(miss_path)
        self.win_sound = pygame.mixer.Sound(win_path)

        # set volume
        self.encounter_sound.set_volume(0.75)
        self.fire_sound.set_volume(0.75)
        self.miss_sound.set_volume(0.75)
        self.win_sound.set_volume(0.75)

    def battle_controls(self, event):
        if self.enemy.is_alive():
            keys = pygame.key.get_pressed()
            self.set_target(keys)
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_SPACE]:
                    self.fire()