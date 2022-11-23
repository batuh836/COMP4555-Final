import os, pygame

class Status:
    def __init__(self):
        self.font = pygame.font.SysFont('monospace', 18)
        self.color = (0, 0, 0)
        self.set_sound()

    def update(self, loop):
        pass

    def check_score(self):
        if self.score >= self.high_score:
            self.high_score = self.score

    def set_sound(self):
        path = os.path.join('assets/sounds/point.wav')
        self.sound = pygame.mixer.Sound(path)
        self.sound.set_volume(0.25)

    def show(self, screen, health):
        health_bar = ""
        for _ in range(health):
            health_bar += "|"
        self.label = self.font.render(f"HP {health_bar}", 1, self.color)
        screen.blit(self.label, (10, screen.get_height() - 20))

    def check_sound(self):
        if self.score % 100 == 0 and self.score != 0:
            self.sound.play()