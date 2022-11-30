import pygame, os

class Effects:
    def __init__(self, settings, screen_width, screen_height):
        self.settings = settings
        self.vfx_size_s = (round(screen_width/18), round(screen_width/18))
        self.vfx_size_m = (round(screen_width/15), round(screen_width/15))
        self.set_sound_effects()
        self.set_visual_effects()

    def play_sfx(self, name):
        sound = self.sfx_dictionary[name]
        self.fx_channel.queue(sound)

    def create_vfx(self, name, location):
        effect = self.vfx_dictionary[name]
        return VFX(effect, location)

    def set_sound_effects(self):
        # set paths
        collide_path = self.settings.get_sfx_setting("collide")
        item_path = self.settings.get_sfx_setting("item")
        player_hit_path = self.settings.get_sfx_setting("player_hit")
        enemy_hit_path = self.settings.get_sfx_setting("enemy_hit")
        enemy_shoot_path = self.settings.get_sfx_setting("enemy_shoot")

        # set sounds
        self.fx_channel = pygame.mixer.Channel(2)
        collide_sound = pygame.mixer.Sound(collide_path)
        item_sound = pygame.mixer.Sound(item_path)
        player_hit_sound = pygame.mixer.Sound(player_hit_path)
        enemy_hit_sound = pygame.mixer.Sound(enemy_hit_path)
        enemy_shoot_sound = pygame.mixer.Sound(enemy_shoot_path)

        # set volume
        collide_sound.set_volume(0.75)
        item_sound.set_volume(0.75)
        player_hit_sound.set_volume(0.75)
        enemy_hit_sound.set_volume(0.75)
        enemy_shoot_sound.set_volume(0.75)

        # add to dictionary
        self.sfx_dictionary = { "collide": collide_sound, 
                                "potion": item_sound, 
                                "player_hit": player_hit_sound,
                                "enemy_hit": enemy_hit_sound,
                                "enemy_shoot": enemy_shoot_sound } 

    def set_visual_effects(self):
        # potion
        potion_effect = []
        potion_effect_path = self.settings.get_vfx_setting("potion")
        for i in range(12):
            path = os.path.join(potion_effect_path, f'potion_{i}.png')
            image = pygame.image.load(path).convert_alpha()
            potion_effect.append(pygame.transform.scale(image, self.vfx_size_m))

        # hit
        hit_effect = []
        hit_effect_path = self.settings.get_vfx_setting("hit")
        for i in range(3):
            path = os.path.join(hit_effect_path, f'hit_{i}.png')
            image = pygame.image.load(path).convert_alpha()
            hit_effect.append(pygame.transform.scale(image, self.vfx_size_m))

        self.vfx_dictionary = {"potion": potion_effect, "hit": hit_effect}

class VFX:
    def __init__(self, frames, location):
        self.frames = frames
        self.location = location
        self.index = 0
        self.current_frame = self.frames[self.index]
    
    def update(self, loop):
        if loop % 4 == 0 and self.index < len(self.frames):
            self.index += 1
            self.current_frame = self.frames[self.index]

    def show(self, screen):
        screen.blit(self.current_frame, self.location)

    def is_complete(self):
        return self.index == len(self.frames) - 1