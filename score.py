import os, pygame

class Score:
    def __init__(self, settings, ts):
        self.settings = settings
        self.total_score = ts
        self.score = 0
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.color = (255, 255, 255)
        self.set_sound()

    def update(self, game):
        if game.state == "end_level":
            self.total_score = self.score + (game.player.health * 100) - (game.obstacles_hit * 100)
        elif game.state == "level":
            if game.loop % 10 == 0:
                self.score += 1
                self.check_sound()

    def show(self, game, screen):
        if game.state == "end_level":
            screen_rect = screen.get_rect()
            label1 = self.font.render(f"COMPLETION TIME: {self.score}", 1, self.color)
            label2 = self.font.render(f"REMAINING HEALTH: {game.player.health}", 1, self.color)
            label3 = self.font.render(f"OBSTACLES HIT: {game.obstacles_hit}", 1, self.color)
            label4 = self.font.render(f"TOTAL SCORE: {self.total_score}", 1, self.color)
            screen.blit(label1, (screen_rect.centerx - label1.get_width()/2, screen_rect.centery - 50))
            screen.blit(label2, (screen_rect.centerx - label2.get_width()/2, screen_rect.centery - 25))
            screen.blit(label3, (screen_rect.centerx - label3.get_width()/2, screen_rect.centery + 25))
            screen.blit(label4, (screen_rect.centerx - label4.get_width()/2, screen_rect.centery + 50))
        else:
            label = self.font.render(f"TOTAL {self.total_score} {self.score}", 1, self.color)
            screen.blit(label, (10, 10))

    def check_sound(self):
        if self.score % 100 == 0 and self.score != 0:
            self.sound.play()

    def set_sound(self):
        path = self.settings.get_sfx_setting("point")
        self.sound = pygame.mixer.Sound(path)
        self.sound.set_volume(0.25)