import os, pygame

class Score:
    def __init__(self, hs):
        self.high_score = hs
        self.score = 0
        self.font = pygame.font.SysFont('monospace', 18)
        self.color = (0, 0, 0)
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

    def show(self, screen):
        self.label = self.font.render(f"HI {self.high_score} {self.score}", 1, self.color)
        label_width = self.label.get_rect().width
        screen.blit(self.label, (screen.get_width() - label_width - 10, 10))

    def check_sound(self):
        if self.score % 100 == 0 and self.score != 0:
            self.sound.play()