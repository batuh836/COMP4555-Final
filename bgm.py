import pygame, os

class BGM:
    def __init__(self, settings):
        self.settings = settings
        self.set_sounds()

    def start_bgm(self):
        self.bgm_channel.play(self.bgm_intro_sound)
        self.bgm_channel.queue(self.bgm_sound)

    def start_boss(self):
        self.bgm_channel.fadeout(3000)
        self.bgm_channel.queue(self.boss_intro_sound)

    def start_victory(self):
        self.bgm_channel.fadeout(3000)
        self.bgm_channel.queue(self.fanfare_intro_sound)

    def update(self, game):
        if game.is_level_complete:
            if not self.bgm_channel.get_busy():
                self.bgm_channel.queue(self.fanfare_sound)
        elif game.in_boss_battle:
            if not self.bgm_channel.get_busy():
                self.bgm_channel.queue(self.boss_sound)
        elif game.is_playing:
            self.bgm_channel.queue(self.bgm_sound)

    def set_sounds(self):
        bgm_intro_path = self.settings.get_level_setting("bgm")[0]
        bgm_path = self.settings.get_level_setting("bgm")[1]
        boss_intro_path = self.settings.get_level_setting("boss_bgm")[0]
        boss_bath = self.settings.get_level_setting("boss_bgm")[1]
        fanfare_intro_path = self.settings.get_level_setting("fanfare")[0]
        fanfare_bath = self.settings.get_level_setting("fanfare")[1]

        self.bgm_channel = pygame.mixer.Channel(0)
        self.bgm_intro_sound = pygame.mixer.Sound(bgm_intro_path)
        self.bgm_sound = pygame.mixer.Sound(bgm_path)
        self.boss_intro_sound = pygame.mixer.Sound(boss_intro_path)
        self.boss_sound = pygame.mixer.Sound(boss_bath)
        self.fanfare_intro_sound = pygame.mixer.Sound(fanfare_intro_path)
        self.fanfare_sound = pygame.mixer.Sound(fanfare_bath)

        self.bgm_intro_sound.set_volume(0.5)
        self.bgm_sound.set_volume(0.5)
        self.boss_intro_sound.set_volume(0.5)
        self.boss_sound.set_volume(0.5)
        self.fanfare_intro_sound.set_volume(0.5)
        self.fanfare_sound.set_volume(0.5)