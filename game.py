import pygame, sys, random
from component import *
from player import *
from battle import *
from score import *
from bg import *
from bgm import *
from effects import *
from shot import *
from settings import *

# screen
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 250
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# states
START_STATE = "start"
INTRO_STATE = "intro"
START_LEVEL_STATE = "start_level"
LEVEL_STATE = "level"
BATTLE_STATE = "battle"
BOSS_STATE = "boss"
END_LEVEL_STATE = "end_level"
GAME_OVER_STATE = "game_over_level"
END_STATE = "end"

class Game:
    def __init__(self, game_state=START_STATE, level = 1, high_score = 0):
        # initialize objects
        self.level = level
        self.settings = Settings(self.level)
        self.bg = [BG(self.settings, 0, screen), BG(self.settings, SCREEN_WIDTH, screen)]
        self.fg = [FG(self.settings, 0, screen), FG(self.settings, SCREEN_WIDTH, screen)]
        self.player = Player(self.settings, screen)
        self.score = Score(self.settings, high_score)
        self.component = Component(self.settings, screen)
        self.battle = Battle(self.settings, self, screen)
        self.bgm = BGM(self.settings)
        self.effects = Effects(self.settings, screen)
        self.shot = Shot(self.settings)

        # game variables
        self.state = game_state
        self.loop = 0
        self.speed = 5
        self.distance = 0
        self.item_timer = 500
        self.boss = None
        # self.boss_distance = self.settings.get_level_setting("boss_distance")
        self.boss_distance = 500
        self.obstacles_hit = 0
        self.component_dist = round(SCREEN_WIDTH/5)

        # game lists
        self.components = []
        self.vfxs = []
        self.player_shots = []
        self.enemy_shots = []

        # show objects
        self.bg[0].show(screen)
        self.player.show(screen)
        self.score.show(self, screen)

        self.set_labels()
        self.set_sound()
        self.spawn_component()

    def set_labels(self):
        self.big_font = pygame.font.SysFont('monospace', 48, bold=True)
        self.small_font = pygame.font.SysFont('monospace', 32)
    
    def start(self):
        self.state = LEVEL_STATE
        self.bgm.start_bgm()

    def start_next_level(self):
        self.__init__(START_LEVEL_STATE, self.level + 1, self.score.total_score)

    def start_battle(self):
        self.state = BATTLE_STATE
        self.battle.start(screen)

    def end_battle(self):
        if self.boss:
            self.state = BOSS_STATE
            self.player.shoot(self)
        else:
            self.state = LEVEL_STATE

    def start_boss(self):
        self.state = BOSS_STATE
        self.boss = Boss(self.settings, screen)
        self.bgm.start_boss()

    def end_level(self):
        self.state = END_LEVEL_STATE
        self.components.clear()
        self.bgm.start_victory()

    def over(self):
        self.state = GAME_OVER_STATE
        self.sound.play()

    def can_spawn(self, loop):
        return loop % 50 == 0 and self.state == LEVEL_STATE or self.state == BOSS_STATE

    def spawn_component(self, component_type = None):
        #list with components
        if len(self.components) > 0:
            prev_component = self.components[-1]
            #calculate distance between obstacles
            dist = prev_component.x + self.player.width + self.component_dist
            x = random.randint(round(dist), round(SCREEN_WIDTH/2 + dist))
        else:
            x = random.randint(SCREEN_WIDTH, round(SCREEN_WIDTH*1.5))

        if component_type == None:
            component_type = random.choice(["obstacle", "enemy"])

        if component_type == "obstacle":
            #create new obstacle
            new_cactus = self.component.create_obstacle(x)
            self.components.append(new_cactus)

        elif component_type == "enemy":
            #chose y value for enemy
            y = random.choice([SCREEN_HEIGHT/2.5, SCREEN_HEIGHT/1.5])
            #create new enemy
            new_enemy = self.component.create_enemy(x, y)
            self.components.append(new_enemy)

        elif component_type == "item":
            #create new item
            new_item = self.component.create_item(x, SCREEN_HEIGHT)
            self.components.append(new_item)

    def collision(self, obj1, obj2):
        if obj1.rect.colliderect(obj2.rect):
            if isinstance(obj1, Player):
                if isinstance(obj2, Enemy_Field):
                    self.components.remove(obj2)
                    self.start_battle()

                elif isinstance(obj2, Obstacle):
                    self.components.remove(obj2)
                    self.player.health -= 1
                    self.obstacles_hit += 1
                    self.player.hit()
                    self.effects.play_sfx("collide")

                elif isinstance(obj2, Item):
                    self.components.remove(obj2)
                    self.player.health += 2
                    self.effects.play_sfx("potion")
                    self.vfxs.append(self.effects.create_vfx("potion", self.player.rect.topleft))

                elif isinstance(obj2, Boss):
                    self.player.hit()
                    self.over()

                elif isinstance(obj2, ShotEffect):
                    self.enemy_shots.remove(obj2)
                    self.player.health -= 2
                    self.player.hit()
                    self.effects.play_sfx("player_hit")

                if not self.player.is_alive():
                    self.over()

            if isinstance(obj1, Boss):
                if isinstance(obj2, ShotEffect):
                    self.player_shots.remove(obj2)
                    self.boss.health -= 1
                    self.boss.dx += 0.1
                    self.boss.shot_time -= 10

                    if self.boss.is_alive():
                        self.boss.knockback()
                        self.effects.play_sfx("enemy_hit")
                        self.vfxs.append(self.effects.create_vfx("hit", self.boss.rect.center))
                        self.spawn_component("item")
                    else:
                        self.end_level()


    def set_sound(self):
        path = self.settings.get_sfx_setting("die")
        self.sound = pygame.mixer.Sound(path)

    def restart(self):
        self.__init__(START_LEVEL_STATE, self.level, self.score.total_score)

    def game_controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.state == START_STATE:
                # start intro
                self.state = START_LEVEL_STATE

            elif self.state == START_LEVEL_STATE:
                self.start()

            elif self.state == LEVEL_STATE or self.state == BOSS_STATE:
                if self.player.on_ground:
                    self.player.jump()

            elif self.state == END_LEVEL_STATE:
                self.start_next_level()

            elif self.state == GAME_OVER_STATE: 
                self.restart()
        # skip to next level
        if keys[pygame.K_UP]:
            if self.state == LEVEL_STATE or self.state == BOSS_STATE:
                self.start_next_level()

    def start_screen(self):
        screen_rect = screen.get_rect()
        label1 = self.big_font.render(f"RPG GO!", 1, (255, 255, 255))
        label2 = self.small_font.render(f"Press SPACE to Start", 1, (255, 255, 255))
        screen.blit(label1, (screen_rect.centerx - label1.get_width()/2, screen_rect.centery))
        screen.blit(label2, (screen_rect.centerx - label1.get_width()/2, screen_rect.centery + 50))

    def run(self):
        # controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == BATTLE_STATE:
                self.battle.battle_controls(event)
            else:
                self.game_controls()

        # game states
        if self.state == START_STATE:
            # show logo
            self.start_screen()

        elif self.state == INTRO_STATE:
            # show intro
            pass

        elif self.state == START_LEVEL_STATE:
            #background
            for bg in self.bg:
                bg.show(screen)

            #foreground
            for fg in self.fg:
                fg.show(screen)
                
            #player
            self.player.show(screen)

        elif self.state == GAME_OVER_STATE:
            # show game over screen
            pass

        elif self.state == END_STATE:
            # show credits
            pass

        else:
            # game loop
            self.loop += 1

            if self.state == BATTLE_STATE:
                # battle
                self.battle.update(self.loop)
                self.battle.show(screen)  

            else:
                # distance 
                self.distance += 1

                # item timer
                if self.state != END_LEVEL_STATE and self.loop % self.item_timer == 0:
                    self.spawn_component("item")  

                if self.state != BOSS_STATE:
                    # increase speed
                    if self.loop % 1000 == 0:
                        self.speed += 0.5

                    # boss timer
                    if self.distance == self.boss_distance:
                        self.start_boss()
                
                #background
                for bg in self.bg:
                    bg.update(-self.speed)
                    bg.show(screen)

                #foreground
                for fg in self.fg:
                    fg.update(-self.speed)
                    fg.show(screen)

                #components
                if self.can_spawn(self.loop):
                    self.spawn_component()

                for component in self.components:
                    # remove obstacle if off screen
                    if component.x < -50:
                        self.components.remove(component)
                    else:
                        component.update(-self.speed, self.loop)
                        component.show(screen)
                        self.collision(self.player, component)
                
                #player
                self.player.update(self.loop)
                self.player.show(screen)

                if self.state == END_LEVEL_STATE:
                    self.player.exit(screen)
                else:
                    self.player.show_health(screen)

                # player shot
                for player_shot in self.player_shots:
                    player_shot.update(self.loop)
                    player_shot.show(screen)
                    self.collision(self.boss, player_shot)

                # boss
                if self.boss:
                    self.boss.update(self)
                    self.boss.show(screen)
                    self.collision(self.player, self.boss)

                    # boss shot
                    for enemy_shot in self.enemy_shots:
                        enemy_shot.update(self.loop)
                        enemy_shot.show(screen)
                        self.collision(self.player, enemy_shot)

            # bgm
            self.bgm.update(self)

            # ui
            self.score.update(self)
            self.score.show(self, screen)

            # vfx
            for vfx in self.vfxs:
                if vfx.is_complete():
                    self.vfxs.remove(vfx)
                else:
                    vfx.update(self.loop)
                    vfx.show(screen)