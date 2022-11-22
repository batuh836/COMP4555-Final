import math
import sys
import pygame
import os
import random
from obstacle import *
from player import *
from battle import *
from score import *
from bg import *

WIDTH = 623
HEIGHT = 150

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('RPG GO!')

class Game:
    def __init__(self, high_score = 0):
        # initialize objects
        self.bg = [BG(0, WIDTH, HEIGHT), BG(WIDTH, WIDTH, HEIGHT)]
        self.player = Player()
        self.score = Score(high_score)
        self.obstacle = Obstacle()
        self.battle = Battle(WIDTH, HEIGHT)

        # show objects
        self.bg[0].show(screen)
        self.player.show(screen)
        self.score.show(screen)

        self.obstacles = []
        self.obstacle_dist = 84
        self.speed = 4
        self.is_playing = False
        self.is_over = False
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

    def over(self):
        self.sound.play()
        screen.blit(self.big_label, (WIDTH // 2 - self.big_label.get_width() // 2, HEIGHT // 4))
        screen.blit(self.small_label, (WIDTH // 2 - self.small_label.get_width() // 2, HEIGHT // 2))
        self.is_playing = False
        self.is_over = True

    def can_spawn(self, loop):
        return loop % 100 == 0

    def spawn_obstacle(self):
        #list with obstacles
        if len(self.obstacles) > 0:
            prev_obstacle = self.obstacles[-1]
            #calculate distance between obstacles
            x = random.randint(prev_obstacle.x + self.player.width + self.obstacle_dist, 
                WIDTH + prev_obstacle.x + self.player.width + self.obstacle_dist)

        #empty
        else:
            x = random.randint(WIDTH + 100, 1000)

        obstacle_type = random.choice([0,1])

        if obstacle_type == 0:
            #create new cactus
            new_cactus = self.obstacle.create_cactus(x)
            self.obstacles.append(new_cactus)
        else:
            #chose y value for bird
            y = random.choice([40, 90])
            #create new bird
            new_bird = self.obstacle.create_bird(x, y)
            self.obstacles.append(new_bird)

    def collision(self, obj1, obj2):
        if obj1.rect.colliderect(obj2.rect):
            if isinstance(obj2, Bird):
                self.battle.start()
                print("collided with bird")
            elif isinstance(obj2, Cactus):
                print("collided with cactus")
            return True

    def set_sound(self):
        path = os.path.join('assets/sounds/die.wav')
        self.sound = pygame.mixer.Sound(path)

    def restart(self):
        self.__init__(self.score.high_score)

def main():
    #objects
    game = Game()
    clock = pygame.time.Clock()
    player = game.player
    loop = 0

    while True:
        if game.is_playing:
            #loop update
            loop += 1

            #bg
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show(screen)
            
            #player
            player.update(loop)
            player.show(screen)

            #obstacles
            if game.can_spawn(loop):
                game.spawn_obstacle()

            for obstacle in game.obstacles:
                obstacle.update(-game.speed)
                obstacle.show(screen)

                #collision
                if game.collision(player, obstacle):
                    game.over()

            game.score.update(loop)
            game.score.show(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game.is_playing and game.is_over:
                        game.restart()
                        player = game.player
                        loop = 0
                    elif not game.is_playing and not game.is_over:
                        game.start()
                    
                    if game.is_playing and not game.is_over and player.on_ground:
                        player.jump()

        clock.tick(60)
        pygame.display.update()

main()