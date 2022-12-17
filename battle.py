import pygame, os, random
from enemy import *

class Battle:
    def __init__(self, settings, game, screen):
        self.settings = settings
        self.game = game
        self.width = round(screen.get_width()*0.9)
        self.height = round(screen.get_height()*0.75)
        self.x = screen.get_width()*0.5 - self.width*0.5
        self.y = screen.get_height()*0.5 - self.height*0.5

        # enemy positions
        self.enemy_speed = self.settings.get_level_setting("enemy_speed")
        enemy_pos_center = (self.width*0.65, self.height*0.5)
        enemy_pos_top = (self.width*0.65, self.height*0.15)
        enemy_pos_bottom = (self.width*0.65, self.height*0.75)
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

        # portrait position
        self.portrait_pos = self.x

        # player attack
        self.attack_limit = 3
        self.attack_cooldown = 100

        self.set_surfaces()
        self.set_rect()
        self.set_sounds()

    def start(self, screen):
        self.fx_channel.play(self.encounter_sound)
        self.player_attack = 3
        self.end_battle_timer = 0
        self.player_target_pos = self.enemy_positions[0]
        self.enemy = Enemy(self.settings)
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

    def show_attack(self, screen):
        for i in range(self.player_attack):
            offset = 40 * i
            position = (self.x + 100 + offset, self.height - 20)
            screen.blit(self.attack, position)
        pass

    def update(self, loop):
        if self.enemy.is_alive():
            # change enemy position
            if loop % self.enemy_speed == 0:
                self.set_enemy_pos()
            # replenish attack
            if self.player_attack < self.attack_limit and loop % self.attack_cooldown == 0:
                self.player_attack += 1
        else:
            self.end()

    def show(self, screen):
        screen.blit(self.bg, (self.x, self.y))
        screen.blit(self.border, (self.x, self.y))
        screen.blit(self.portrait, (self.x + 20, self.height - 60))
        if self.enemy.is_alive():
            self.show_attack(screen)
            self.enemy.show_health(screen)
            screen.blit(self.enemy.surface, self.enemy_current_pos)
            screen.blit(self.target, self.player_target_pos)

    def set_surfaces(self):
        border_path = self.settings.get_image_setting("battle_border")
        bg_path = self.settings.get_level_setting("battle_bg")
        target_path = self.settings.get_image_setting("target")
        attack_path = self.settings.get_image_setting("attack")
        portrait_path = self.settings.get_player_setting("portrait")

        border_image = pygame.image.load(border_path).convert_alpha()
        bg_image = pygame.image.load(bg_path).convert_alpha()
        target_image = pygame.image.load(target_path).convert_alpha()
        attack_image = pygame.image.load(attack_path).convert_alpha()
        portrait_image = pygame.image.load(portrait_path).convert_alpha()

        self.border = pygame.transform.scale(border_image, (self.width, self.height))
        self.bg = pygame.transform.scale(bg_image, (self.width, self.height))
        self.target = pygame.transform.scale(target_image, (75, 75))
        self.attack = pygame.transform.scale(attack_image, (30, 30))
        self.portrait = pygame.transform.scale(portrait_image, (75, 75))

        self.overlay_colour = (0, 0, 0, 0)

    def set_rect(self):
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def fire(self):
        if self.player_attack > 0:
            self.fx_channel.stop()
            self.fx_channel.play(self.fire_sound)

            if self.player_target_pos == self.enemy_current_pos:
                self.enemy.health -= 1
                self.fx_channel.queue(self.hit_sound)
                self.game.vfxs.append(self.game.effects.create_vfx("hit", self.enemy_current_pos))
            else:
                self.player_attack -= 1
                self.fx_channel.queue(self.miss_sound)
        else:
            self.fx_channel.stop()
            self.fx_channel.play(self.error_sound)

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
        encounter_path = self.settings.get_sfx_setting("encounter")
        fire_path = self.settings.get_sfx_setting("fire")
        hit_path = self.settings.get_sfx_setting("hit")
        miss_path = self.settings.get_sfx_setting("miss")
        win_path = self.settings.get_sfx_setting("win")
        error_path = self.settings.get_sfx_setting("error")

        # set sounds
        self.fx_channel = pygame.mixer.Channel(1)
        self.encounter_sound = pygame.mixer.Sound(encounter_path)
        self.fire_sound = pygame.mixer.Sound(fire_path)
        self.hit_sound = pygame.mixer.Sound(hit_path)
        self.miss_sound = pygame.mixer.Sound(miss_path)
        self.win_sound = pygame.mixer.Sound(win_path)
        self.error_sound = pygame.mixer.Sound(error_path)

        # set volume
        self.encounter_sound.set_volume(0.5)
        self.fire_sound.set_volume(0.25)
        self.miss_sound.set_volume(0.25)
        self.win_sound.set_volume(0.5)
        self.error_sound.set_volume(0.25)

    def battle_controls(self, event):
        if self.enemy.is_alive():
            keys = pygame.key.get_pressed()
            self.set_target(keys)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.fire()