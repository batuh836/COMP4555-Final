import pygame, os

class Effects:
    def __init__(self, screen_width, screen_height):
        self.vfx_size_m = (round(screen_width/15), round(screen_width/15))
        self.set_sound_effects()
        self.set_visual_effects()

    def play_sfx(self, name):
        sound = self.sfx_dictionary[name]
        self.fx_channel.queue(sound)

    def create_vfx(self, name):
        effect = self.vfx_dictionary[name]
        return VFX(effect)

    def set_sound_effects(self):
        # set paths
        collide_path = os.path.join('assets/sounds/collide.wav')
        item_path = os.path.join('assets/sounds/item.wav')

        # set sounds
        self.fx_channel = pygame.mixer.Channel(1)
        collide_sound = pygame.mixer.Sound(collide_path)
        item_sound = pygame.mixer.Sound(item_path)

        # set volume
        collide_sound.set_volume(0.75)

        # add to dictionary
        self.sfx_dictionary = {"collide": collide_sound, "potion": item_sound} 

    def set_visual_effects(self):
        # potion
        potion_effect = []
        for i in range(12):
            path = os.path.join(f'assets/images/effects/potion_effect/potion_{i}.png')
            image = pygame.image.load(path).convert_alpha()
            potion_effect.append(pygame.transform.scale(image, self.vfx_size_m))
        self.vfx_dictionary = {"potion": potion_effect}

class VFX:
    def __init__(self, frames):
        self.frames = frames
        self.index = 0
        self.current_frame = self.frames[self.index]
    
    def update(self, loop):
        if loop % 4 == 0 and self.index < len(self.frames):
            self.index += 1
            self.current_frame = self.frames[self.index]

    def show(self, screen, location):
        screen.blit(self.current_frame, location)

    def is_complete(self):
        return self.index == len(self.frames) - 1