import sys
import pygame
import os
import random
from component import *
from player import *
from battle import *
from score import *
from bg import *
from bgm import *
from effects import *

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
        self.fg = [FG(0, WIDTH, HEIGHT), FG(WIDTH, WIDTH, HEIGHT)]
        self.player = Player(WIDTH, HEIGHT)
        self.score = Score(high_score)
        self.obstacle = Component(WIDTH, HEIGHT)
        self.battle = Battle(self, WIDTH, HEIGHT)
        self.bgm = BGM()
        self.effects = Effects(WIDTH, HEIGHT)
        self.loop = 0
        self.speed = 5

        # show objects
        self.bg[0].show(screen)
        self.player.show(screen)
        self.score.show(screen)

        self.components = []
        self.component_dist = round(WIDTH/10)
        self.vfxs = []
        self.is_playing = False
        self.is_over = False
        self.in_battle = False
        self.set_labels()
        self.set_sound()
        self.spawn_obstacle()

    def set_labels(self):
        big_font = pygame.font.SysFont('monospace', 24, bold=True)
        small_font = pygame.font.SysFont('monospace', 18)
        self.big_label = big_font.render(f'G A M E O V E R', 1, (255, 255, 255))
        self.small_label = small_font.render(f'Press Space to Restart', 1, (255, 255, 255))
    
    def start(self):
        self.is_playing = True
        self.is_over = False
        self.bgm.start()

    def start_battle(self):
        self.is_playing = False
        self.in_battle = True
        self.battle.start(screen)

    def end_battle(self):
        self.is_playing = True
        self.in_battle = False

    def over(self):
        self.sound.play()
        screen.blit(self.big_label, (WIDTH // 2 - self.big_label.get_width() // 2, HEIGHT // 4))
        screen.blit(self.small_label, (WIDTH // 2 - self.small_label.get_width() // 2, HEIGHT // 2))
        self.is_playing = False
        self.is_over = True

    def can_spawn(self, loop):
        return loop % 50 == 0

    def spawn_obstacle(self):
        #list with components
        if len(self.components) > 0:
            prev_obstacle = self.components[-1]
            #calculate distance between obstacles
            dist = prev_obstacle.x + self.player.width + self.component_dist
            x = random.randint(dist, round(WIDTH/2 + dist))

        #empty
        else:
            x = random.randint(WIDTH, round(WIDTH*1.5))

        obstacle_type = random.choice([0, 1, 2])
        # obstacle_type = 2

        if obstacle_type == 0:
            #create new obstacle
            new_cactus = self.obstacle.create_obstacle(x)
            self.components.append(new_cactus)
        elif obstacle_type == 1:
            #chose y value for enemy
            y = random.choice([HEIGHT/2.5, HEIGHT/1.5])
            #create new enemy
            new_enemy = self.obstacle.create_enemy(x, y)
            self.components.append(new_enemy)
        elif obstacle_type == 2:
            #create new item
            new_item = self.obstacle.create_item(x, HEIGHT)
            self.components.append(new_item)

    def collision(self, player, component):
        if player.rect.colliderect(component.rect):
            if isinstance(component, Enemy):
                print("collided with enemy")
                self.components.clear()
                self.start_battle()
            elif isinstance(component, Obstacle):
                self.components.remove(component)
                self.player.health -= 1
                self.effects.play_sfx("collide")
            elif isinstance(component, Item):
                self.components.remove(component)
                self.player.health += 1
                self.effects.play_sfx("potion")
                self.vfxs.append(self.effects.create_vfx("potion"))

    def set_sound(self):
        path = os.path.join('assets/sounds/die.wav')
        self.sound = pygame.mixer.Sound(path)

    def restart(self):
        self.__init__(self.score.high_score)

    def game_controls(self):
        keys = pygame.key.get_pressed()
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

    while True:
        #loop update
        game.loop += 1

        if game.in_battle:
            game.battle.update(game.loop)
            game.battle.show(screen)
            
        elif game.is_playing:
            # increase speed
            if game.loop % 1000 == 0:
                game.speed += 1

            #background
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show(screen)

            #foreground
            for fg in game.fg:
                fg.update(-game.speed)
                fg.show(screen)
            
            #player
            if game.player.is_alive():
                game.player.update(game.loop)
                game.player.show(screen)
            else:
                game.over()

            #components
            if game.can_spawn(game.loop):
                game.spawn_obstacle()

            for component in game.components:
                # remove obstacle if off screen
                if component.x < -50:
                    game.components.remove(component)
                else:
                    component.update(-game.speed)
                    component.show(screen)
                    game.collision(game.player, component)

            # bgm
            if game.in_battle or game.is_playing:
                game.bgm.update()
            
        # ui
        game.score.update(game.loop)
        game.score.show(screen)
        game.player.show_health(screen)

        # vfx
        for vfx in game.vfxs:
            if vfx.is_complete():
                game.vfxs.remove(vfx)
            else:
                vfx.update(game.loop)
                vfx.show(screen, (game.player.x, game.player.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # controls
            if game.in_battle:
                game.battle.battle_controls(event)
            else:
                game.game_controls()

        clock.tick(60)
        pygame.display.update()

main()