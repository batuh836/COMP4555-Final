import os, pygame, math

class Score:
    def __init__(self, settings, ts):
        self.settings = settings
        self.total_score = ts
        self.time = 0
        self.big_font = pygame.font.SysFont('monospace', 30, bold=True)
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.color = (255, 255, 255)

    def update(self, game):
        if game.state == "level" or game.state == "battle" or game.state == "boss":
            if game.loop % 10 == 0:
                self.time += 1

    def show(self, game, screen):
        if game.state == "end_level":
            screen_rect = screen.get_rect()

            label0 = self.big_font.render("LEVEL COMPLETE", 1, self.color)
            label1 = self.font.render(f"COMPLETION TIME: {self.time}", 1, self.color)
            label2 = self.font.render(f"REMAINING HEALTH: {game.player.health}", 1, self.color)
            label3 = self.font.render(f"OBSTACLES HIT: {game.obstacles_hit}", 1, self.color)
            label4 = self.font.render(f"TOTAL SCORE: {self.total_score}", 1, self.color)

            screen.blit(label0, (screen_rect.centerx - label0.get_width()/2, screen_rect.centery - 75))
            screen.blit(label1, (screen_rect.centerx - label1.get_width()/2, screen_rect.centery - 25))
            screen.blit(label2, (screen_rect.centerx - label2.get_width()/2, screen_rect.centery))
            screen.blit(label3, (screen_rect.centerx - label3.get_width()/2, screen_rect.centery + 25))
            screen.blit(label4, (screen_rect.centerx - label4.get_width()/2, screen_rect.centery + 75))

        elif game.state == "level" or game.state == "boss":
            label = self.font.render(f"SCORE: {self.total_score} TIME: {self.time}", 1, self.color)
            screen.blit(label, (10, 10))

    def calculate_score(self, game):
        boss_completion = 2500
        time_score = round((game.boss_distance + boss_completion)/10 - self.time) * 10
        health_score = game.player.health * 100
        obstacle_penalty = game.obstacles_hit * 100
        self.total_score += time_score + health_score - obstacle_penalty