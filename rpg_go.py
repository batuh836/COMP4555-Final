import sys
import pygame
import os
import random
from obstacle import *
from player import *
from battle import *
from score import *
from bg import *

# pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('RPG GO!')

# screen
WIDTH = 750
HEIGHT = 250
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Game:
    def __init__(self, high_score = 0):
        # initialize objects
        self.bg = [BG(0, WIDTH, HEIGHT), BG(WIDTH, WIDTH, HEIGHT)]
        self.player = Player(WIDTH, HEIGHT)
        self.score = Score(high_score)
        self.obstacle = Obstacle(WIDTH, HEIGHT)
        self.battle = Battle(WIDTH, HEIGHT)
        self.loop = 0

        # show objects
        self.bg[0].show(screen)
        self.player.show(screen)
        self.score.show(screen)

        self.obstacles = []
        self.obstacle_dist = round(WIDTH/10)
        self.speed = 5
        self.is_playing = False
        self.is_over = False
        self.in_battle = False
        self.set_labels()
        self.set_sound()
        self.spawn_obstacle()

    def set_labels(self):
        big_font = pygame.font.SysFont('monospace', 24, bold=True)
        small_font = pygame.font.SysFont('monospace', 18)
        self.big_label = big_font.render(f'G A M E O V E R', 1, (0, 0, 0))
        self.small_label = small_font.render(f'Press Space to Restart', 1, (0, 0, 0))
    
    def start(self):
        self.is_playing = True
        self.is_over = False

    def start_battle(self):
        self.is_playing = False
        self.in_battle = True
        self.battle.start(screen)

    def end_battle(self):
        self.is_playing = True
        self.in_battle = False
        # self.battle.end(screen)

    def over(self):
        self.sound.play()
        screen.blit(self.big_label, (WIDTH // 2 - self.big_label.get_width() // 2, HEIGHT // 4))
        screen.blit(self.small_label, (WIDTH // 2 - self.small_label.get_width() // 2, HEIGHT // 2))
        self.is_playing = False
        self.is_over = True

    def can_spawn(self, loop):
        return loop % 50 == 0

    def spawn_obstacle(self):
        #list with obstacles
        if len(self.obstacles) > 0:
            prev_obstacle = self.obstacles[-1]
            #calculate distance between obstacles
            dist = prev_obstacle.x + self.player.width + self.obstacle_dist
            x = random.randint(dist, round(WIDTH/2 + dist))

        #empty
        else:
            x = random.randint(WIDTH, round(WIDTH*1.5))

        obstacle_type = random.choice([0,1])

        if obstacle_type == 0:
            #create new cactus
            new_cactus = self.obstacle.create_cactus(x)
            self.obstacles.append(new_cactus)
        else:
            #chose y value for bird
            y = random.choice([HEIGHT/2.5, HEIGHT/1.5])
            #create new bird
            new_bird = self.obstacle.create_bird(x, y)
            self.obstacles.append(new_bird)

    def collision(self, obj1, obj2):
        if obj1.rect.colliderect(obj2.rect):
            if isinstance(obj2, Bird):
                self.start_battle()
            elif isinstance(obj2, Cactus):
                # self.over()
                pass

    def set_sound(self):
        path = os.path.join('assets/sounds/die.wav')
        self.sound = pygame.mixer.Sound(path)

    def restart(self):
        self.__init__(self.score.high_score)

    def game_controls(self, keys):
        if keys[pygame.K_SPACE]:
            if not self.is_playing and self.is_over:
                self.restart()
            elif not self.is_playing and not self.is_over:
                self.start()
            
            if self.is_playing and not self.is_over and self.player.on_ground:
                self.player.jump()

def main():
    #objects
    game = Game()
    clock = pygame.time.Clock()
    player = game.player

    while True:
        if game.in_battle:
            game.battle.show(screen)
            
        elif game.is_playing:
            #loop update
            game.loop += 1

            #bg
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show(screen)
            
            #player
            player.update(game.loop)
            player.show(screen)

            #obstacles
            if game.can_spawn(game.loop):
                game.spawn_obstacle()

            for obstacle in game.obstacles:
                # remove obstacle if off screen
                if obstacle.x < -50:
                    game.obstacles.remove(obstacle)
                    print(len(game.obstacles))
                else:
                    obstacle.update(-game.speed)
                    obstacle.show(screen)
                    game.collision(player, obstacle)

            game.score.update(game.loop)
            game.score.show(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # controls
            keys = pygame.key.get_pressed()
            if game.in_battle:
                game.battle.battle_controls(keys)
            else:
                game.game_controls(keys)

        clock.tick(60)
        pygame.display.update()

main()