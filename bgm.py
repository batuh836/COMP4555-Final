import pygame, os

class BGM:
    def __init__(self):
        self.set_sounds()

    def start_bgm(self):
        self.bgm_channel.play(self.bgm_intro_sound)
        self.bgm_channel.queue(self.bgm_sound)

    def start_boss(self):
        self.bgm_channel.fadeout(3000)
        self.bgm_channel.queue(self.boss_intro_sound)

    def start_victory(self):
        self.bgm_channel.fadeout(3000)
        # queue victory song

    def update(self, game):
        if game.is_level_complete:
            if not self.bgm_channel.get_busy():
                # queue victory song
                pass
        elif game.in_boss_battle:
            if not self.bgm_channel.get_busy():
                self.bgm_channel.queue(self.boss_sound)
        elif game.is_playing:
            self.bgm_channel.queue(self.bgm_sound)

    def set_sounds(self):
        bgm_intro_path = os.path.join('assets/sounds/bgm/bgm_intro_00.wav')
        bgm_path = os.path.join('assets/sounds/bgm/bgm_00.wav')
        boss_intro_path = os.path.join('assets/sounds/bgm/boss_intro_00.wav')
        boss_bath = os.path.join('assets/sounds/bgm/boss_00.wav')

        self.bgm_channel = pygame.mixer.Channel(0)
        self.bgm_intro_sound = pygame.mixer.Sound(bgm_intro_path)
        self.bgm_sound = pygame.mixer.Sound(bgm_path)
        self.boss_intro_sound = pygame.mixer.Sound(boss_intro_path)
        self.boss_sound = pygame.mixer.Sound(boss_bath)

        self.bgm_intro_sound.set_volume(0.5)
        self.bgm_sound.set_volume(0.5)
        self.boss_intro_sound.set_volume(0.5)
        self.boss_sound.set_volume(0.5)