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
from shot import *
from settings import *

# pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('RPG GO!')

# screen
WIDTH = 750
HEIGHT = 250
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Game:
    def __init__(self, level = 1, high_score = 0):
        # initialize objects
        print(level)
        self.level = level
        self.settings = Settings(self.level)
        self.bg = [BG(self.settings, 0, WIDTH, HEIGHT), BG(self.settings, WIDTH, WIDTH, HEIGHT)]
        self.fg = [FG(self.settings, 0, WIDTH, HEIGHT), FG(self.settings, WIDTH, WIDTH, HEIGHT)]
        self.player = Player(self.settings, WIDTH, HEIGHT)
        self.score = Score(self.settings, high_score)
        self.component = Component(self.settings, WIDTH, HEIGHT)
        self.battle = Battle(self.settings, self, WIDTH, HEIGHT)
        self.bgm = BGM(self.settings)
        self.effects = Effects(self.settings, WIDTH, HEIGHT)
        self.shot = Shot(self.settings)

        # game variables
        self.loop = 0
        self.speed = 5
        self.distance = 0
        self.item_timer = 500
        self.boss_distance = 1000
        self.obstacles_hit = 0

        self.components = []
        self.component_dist = round(WIDTH/10)
        self.vfxs = []
        self.is_playing = False
        self.is_over = False
        self.in_battle = False
        self.in_boss_battle = False
        self.is_level_complete = False
        self.player_shot = None
        self.enemy_shot = None

        # show objects
        self.bg[0].show(screen)
        self.player.show(screen)
        self.score.show(self, screen)

        self.set_labels()
        self.set_sound()
        self.spawn_component()

    def set_labels(self):
        big_font = pygame.font.SysFont('monospace', 24, bold=True)
        small_font = pygame.font.SysFont('monospace', 18)
        self.big_label = big_font.render(f'G A M E O V E R', 1, (255, 255, 255))
        self.small_label = small_font.render(f'Press Space to Restart', 1, (255, 255, 255))
    
    def start(self):
        self.is_playing = True
        self.is_over = False
        self.bgm.start_bgm()

    def start_next_level(self):
        self.__init__(self.level + 1, self.score.total_score)

    def start_battle(self):
        self.in_battle = True
        self.battle.start(screen)

    def end_battle(self):
        self.in_battle = False
        if self.in_boss_battle:
            self.player_shot = self.player.shoot(self.shot)

    def start_boss(self):
        self.in_boss_battle = True
        self.boss = Boss(self.settings, WIDTH, HEIGHT)
        self.bgm.start_boss()

    def end_level(self):
        self.is_level_complete = True
        self.components.clear()
        self.bgm.start_victory()

    def over(self):
        self.sound.play()
        screen.blit(self.big_label, (WIDTH // 2 - self.big_label.get_width() // 2, HEIGHT // 4))
        screen.blit(self.small_label, (WIDTH // 2 - self.small_label.get_width() // 2, HEIGHT // 2))
        self.is_playing = False
        self.is_over = True

    def can_spawn(self, loop):
        return loop % 50 == 0 and not self.is_level_complete

    def spawn_component(self, component_type = None):
        #list with components
        if len(self.components) > 0:
            prev_component = self.components[-1]
            #calculate distance between obstacles
            dist = prev_component.x + self.player.width + self.component_dist
            x = random.randint(dist, round(WIDTH/2 + dist))
        else:
            x = random.randint(WIDTH, round(WIDTH*1.5))

        if component_type == None:
            if self.in_boss_battle:
                component_type = "enemy"
            else:
                component_type = random.choice(["obstacle", "enemy"])

        if component_type == "obstacle":
            #create new obstacle
            new_cactus = self.component.create_obstacle(x)
            self.components.append(new_cactus)
        elif component_type == "enemy":
            #chose y value for enemy
            y = random.choice([HEIGHT/2.5, HEIGHT/1.5])
            #create new enemy
            new_enemy = self.component.create_enemy(x, y)
            self.components.append(new_enemy)
        elif component_type == "item":
            #create new item
            new_item = self.component.create_item(x, HEIGHT)
            self.components.append(new_item)

    def collision(self, obj1, obj2):
        if obj1.rect.colliderect(obj2.rect):
            if isinstance(obj1, Player):
                if isinstance(obj2, Enemy_Field):
                    self.components.clear()
                    self.start_battle()

                elif isinstance(obj2, Obstacle):
                    self.components.remove(obj2)
                    self.player.health -= 1
                    self.obstacles_hit += 1
                    self.player.hit()
                    self.effects.play_sfx("collide")

                elif isinstance(obj2, Item):
                    self.components.remove(obj2)
                    self.player.health += 1
                    self.effects.play_sfx("potion")
                    self.vfxs.append(self.effects.create_vfx("potion", self.player.rect.topleft))

                elif isinstance(obj2, Boss):
                    self.over()

                elif isinstance(obj2, ShotEffect):
                    self.enemy_shot = None
                    self.player.health -= 2
                    self.player.hit()
                    self.effects.play_sfx("player_hit")

            if isinstance(obj1, Boss):
                if isinstance(obj2, ShotEffect):
                    self.player_shot = None
                    self.boss.health -= 1
                    self.boss.dx += 0.5
                    self.boss.shot_time -= 10

                    if self.boss.is_alive():
                        self.effects.play_sfx("enemy_hit")
                        self.vfxs.append(self.effects.create_vfx("hit", self.boss.rect.center))
                        self.spawn_component("item")
                    else:
                        self.end_level()


    def set_sound(self):
        path = self.settings.get_sfx_setting("die")
        self.sound = pygame.mixer.Sound(path)

    def restart(self):
        self.__init__(self.level, self.score.high_score)

    def game_controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.is_playing:
                if self.is_level_complete and not self.in_boss_battle:
                    self.start_next_level()
                if self.player.on_ground:
                    self.player.jump()
            else: 
                if self.is_over:
                    self.restart()
                else:
                    self.start()

def main():
    #objects
    game = Game()
    clock = pygame.time.Clock()

    while True:
        #loop update
        game.loop += 1
            
        if game.is_playing:
            # puase movement during battle
            if game.in_battle:
                game.battle.update(game.loop)
                game.battle.show(screen)
            else:
                # distance update
                if not game.is_level_complete:
                    game.distance += 1

                    if not game.in_boss_battle:
                        # increase speed
                        if game.loop % 1000 == 0:
                            game.speed += 1

                        # boss timer
                        if game.distance == game.boss_distance:
                            game.start_boss()

                        # item timer
                        if game.loop % game.item_timer == 0:
                            game.spawn_component("item")

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
                    if game.is_level_complete:
                        game.player.x += 5
                    game.player.update(game.loop)
                    game.player.show(screen)
                    game.player.show_health(screen)
                else:
                    game.over()

                #components
                if game.can_spawn(game.loop):
                    game.spawn_component()

                for component in game.components:
                    # remove obstacle if off screen
                    if component.x < -50:
                        game.components.remove(component)
                    else:
                        component.update(-game.speed)
                        component.show(screen)
                        game.collision(game.player, component)

                # boss
                if game.in_boss_battle:
                    game.boss.update(game.loop)
                    game.boss.show(screen)
                    game.boss.show_health(screen)

                    # boss defeat
                    if game.boss.is_alive():
                        game.collision(game.player, game.boss)

                        # player shot
                        if game.player_shot:
                            game.player_shot.update(game.loop)
                            game.player_shot.show(screen)
                            game.collision(game.boss, game.player_shot)

                        # enemy shot
                        if game.boss.can_shoot:
                            game.effects.play_sfx("enemy_shoot")
                            game.enemy_shot = game.boss.shoot(game.shot)
                    
                        if game.enemy_shot:
                            game.enemy_shot.update(game.loop)
                            game.enemy_shot.show(screen)
                            game.collision(game.player, game.enemy_shot)
                    else:
                        if game.boss.surface.get_alpha() > 0 and game.loop % 20 == 0:
                            boss_rect = game.boss.rect
                            effect_location = random.choice([
                                boss_rect.center,
                                boss_rect.topleft,
                                boss_rect.topright,
                                boss_rect.bottomleft,
                                boss_rect.bottomright
                            ])
                            game.vfxs.append(game.effects.create_vfx("hit", effect_location))
                            game.effects.play_sfx("enemy_hit")
                        elif game.boss.surface.get_alpha() == 0:
                            game.in_boss_battle = False             

        # bgm
        game.bgm.update(game)

        # ui
        game.score.update(game, game.loop)
        game.score.show(game, screen)

        # vfx
        for vfx in game.vfxs:
            if vfx.is_complete():
                game.vfxs.remove(vfx)
            else:
                vfx.update(game.loop)
                vfx.show(screen)

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