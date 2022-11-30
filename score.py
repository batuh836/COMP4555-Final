import os, pygame

class Score:
    def __init__(self, settings, hs):
        self.settings = settings
        self.high_score = hs
        self.score = 0
        self.level_score = hs
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.color = (255, 255, 255)
        self.set_sound()

    def update(self, game, loop):
        if game.is_level_complete:
            self.level_score = self.score + (game.player.health * 100) - (game.obstacles_hit * 100)
        elif game.is_playing:
            if loop % 10 == 0:
                self.score += 1
                self.check_score()
                self.check_sound()

    def show(self, game, screen):
        if game.is_level_complete and not game.in_boss_battle:
            screen_rect = screen.get_rect()
            label1 = self.font.render(f"COMPLETION TIME: {self.score}", 1, self.color)
            label2 = self.font.render(f"REMAINING HEALTH: {game.player.health}", 1, self.color)
            label3 = self.font.render(f"OBSTACLES HIT: {game.obstacles_hit}", 1, self.color)
            label4 = self.font.render(f"TOTAL SCORE: {self.level_score}", 1, self.color)
            screen.blit(label1, (screen_rect.centerx - label1.get_width()/2, screen_rect.centery - 50))
            screen.blit(label2, (screen_rect.centerx - label2.get_width()/2, screen_rect.centery - 25))
            screen.blit(label3, (screen_rect.centerx - label3.get_width()/2, screen_rect.centery + 25))
            screen.blit(label4, (screen_rect.centerx - label4.get_width()/2, screen_rect.centery + 50))
        else:
            label = self.font.render(f"HI {self.high_score} {self.score}", 1, self.color)
            screen.blit(label, (10, 10))

    def check_sound(self):
        if self.score % 100 == 0 and self.score != 0:
            self.sound.play()

    def check_score(self):
        if self.score >= self.high_score:
            self.high_score = self.score

    def set_sound(self):
        path = self.settings.get_sfx_setting("point")
        self.sound = pygame.mixer.Sound(path)
        self.sound.set_volume(0.25)