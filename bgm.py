import pygame, os

class BGM:
    def __init__(self):
        self.set_sounds()

    def start(self):
        self.bgm_channel.play(self.intro_sound)
        self.bgm_channel.queue(self.bgm_sound)

    def update(self):
        self.bgm_channel.queue(self.bgm_sound)

    def set_sounds(self):
        intro_path = os.path.join('assets/sounds/bgm/bgm_intro_00.wav')
        bgm_path = os.path.join('assets/sounds/bgm/bgm_00.wav')

        self.bgm_channel = pygame.mixer.Channel(0)
        self.intro_sound = pygame.mixer.Sound(intro_path)
        self.bgm_sound = pygame.mixer.Sound(bgm_path)

        self.intro_sound.set_volume(0.5)
        self.bgm_sound.set_volume(0.5)