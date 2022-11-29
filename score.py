import os, pygame

class Score:
    def __init__(self, hs):
        self.high_score = hs
        self.score = 0
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.color = (255, 255, 255)
        self.set_sound()

    def update(self, loop):
        self.score = loop // 10
        self.check_score()
        self.check_sound()

    def check_score(self):
        if self.score >= self.high_score:
            self.high_score = self.score

    def set_sound(self):
        path = os.path.join('assets/sounds/point.wav')
        self.sound = pygame.mixer.Sound(path)
        self.sound.set_volume(0.25)

    def show(self, screen):
        self.label = self.font.render(f"HI {self.high_score} {self.score}", 1, self.color)
        screen.blit(self.label, (10, 10))

    def check_sound(self):
        if self.score % 100 == 0 and self.score != 0:
            self.sound.play()