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
from overlay import *

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
END_BOSS_STATE = "end_boss"
END_LEVEL_STATE = "end_level"
GAME_OVER_STATE = "game_over_level"
END_STATE = "end"

class Game:
    def __init__(self, game_state=START_STATE, level = 1, total_score = 0):
        # initialize objects
        self.level = level
        self.settings = Settings(self.level)
        self.bg = [BG(self.settings, 0, screen), BG(self.settings, SCREEN_WIDTH, screen)]
        self.fg = [FG(self.settings, 0, screen), FG(self.settings, SCREEN_WIDTH, screen)]
        self.overlay = Overlay(screen)
        self.player = Player(self.settings, screen)
        self.score = Score(self.settings, total_score)
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
        self.boss_distance = self.settings.get_level_setting("boss_distance")
        # self.boss_distance = 500
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
        self.overlay.show(screen)

        self.set_labels()
        self.set_sound()

    def set_labels(self):
        self.big_font = pygame.font.SysFont('monospace', 48, bold=True)
        self.small_font = pygame.font.SysFont('monospace', 32, bold=True)
        self.logo = pygame.image.load("assets/images/misc/logo.png").convert_alpha()

    def setup_level(self):
        self.state = START_LEVEL_STATE
        self.effects.play_sfx("potion")
        self.overlay.fade_out()
    
    def start_level(self):
        self.state = LEVEL_STATE
        self.bgm.start_bgm()

    def start_next_level(self):
        self.bgm.end_bgm()
        self.__init__(START_STATE, self.level + 1, self.score.total_score)

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

    def end_boss(self):
        self.state = END_BOSS_STATE
        self.score.calculate_score(self)
        self.enemy_shots.clear()
        self.components.clear()
        self.bgm.start_victory()

    def end_level(self):
        self.state = END_LEVEL_STATE
        self.boss = None
        self.overlay.fade_in()

    def end_game(self):
        self.state = END_STATE
        self.bgm.start_victory()

    def over(self):
        self.state = GAME_OVER_STATE
        self.bgm.end_bgm()
        self.overlay.fade_in()

    def restart(self):
        self.__init__(START_STATE, self.level, self.score.total_score)

    def can_spawn(self):
        return self.loop % 50 == 0 and self.state == LEVEL_STATE or self.state == BOSS_STATE

    def spawn_component(self, component_type = "", amount = 1):
        for _ in range(amount):
            if len(self.components) > 0:
                last_component = self.components[-1]
                #calculate distance between obstacles
                dist = last_component.x + self.player.width + self.component_dist
                x = random.randint(round(dist), round(SCREEN_WIDTH/3 + dist))
            else:
                x = random.randint(SCREEN_WIDTH, round(SCREEN_WIDTH * 1.5))

            if component_type == "":
                num_enemies = 0
                num_obstacles = 0

                for component in self.components:
                    if isinstance(component, Enemy_Field):
                        num_enemies += 1
                    if isinstance(component, Obstacle):
                        num_obstacles += 1

                if num_enemies > num_obstacles:
                    component_type = "obstacle"
                elif num_enemies < num_obstacles:
                    component_type = "enemy"
                else:
                    component_type = random.choice(["obstacle", "enemy"])

            if component_type == "obstacle":
                #create new obstacle
                new_cactus = self.component.create_obstacle(x)
                self.components.append(new_cactus)

            if component_type == "enemy":
                #chose y value for enemy
                y = random.choice([SCREEN_HEIGHT/2.5, SCREEN_HEIGHT/1.5])
                #create new enemy
                new_enemy = self.component.create_enemy(x, y)
                self.components.append(new_enemy)

            if component_type == "item":
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
                    self.player.health -= self.boss.strength
                    self.player.hit()
                    self.effects.play_sfx("player_hit")

                if not self.player.is_alive():
                    self.over()

            if isinstance(obj1, Boss):
                if isinstance(obj2, ShotEffect):
                    self.player_shots.remove(obj2)
                    self.boss.health -= 1
                    self.boss.dx += 0.25
                    self.boss.shot_time -= 10

                    if self.boss.is_alive():
                        self.boss.knockback()
                        self.effects.play_sfx("enemy_hit")
                        self.vfxs.append(self.effects.create_vfx("hit", self.boss.rect.center))
                        self.spawn_component("item")
                    else:
                        self.end_boss()

    def set_sound(self):
        path = self.settings.get_sfx_setting("die")
        self.sound = pygame.mixer.Sound(path)

    def game_controls(self, event):
        if event.type == pygame.KEYDOWN and not self.overlay.is_transitioning():
            if event.key == pygame.K_SPACE:
                if self.state == START_STATE:
                    self.setup_level()

                elif self.state == START_LEVEL_STATE:
                    self.start_level()

                elif self.state == LEVEL_STATE or self.state == BOSS_STATE:
                    if self.player.on_ground:
                        self.player.jump()

                elif self.state == END_LEVEL_STATE:
                    if self.level == 5:
                        self.end_game()
                    else:
                        self.start_next_level()

                elif self.state == GAME_OVER_STATE: 
                    self.restart()
            # skip to next level
            if event.key == pygame.K_UP:
                if self.state == START_LEVEL_STATE or self.state == LEVEL_STATE:
                    self.start_next_level()

    def start_screen(self):
        screen_rect = screen.get_rect()

        if self.level == 1:
            label = self.small_font.render(f"Press SPACE to Start", 1, (255, 255, 255))
            screen.blit(self.logo, (screen_rect.centerx - self.logo.get_width()/2, 25))
            screen.blit(label, (screen_rect.centerx - label.get_width()/2, screen_rect.centery + 75))
        else:
            label1 = self.big_font.render(f"LEVEL {self.level}", 1, (255, 255, 255))
            label2 = self.small_font.render(f"Press SPACE to Start", 1, (255, 255, 255))
            screen.blit(label1, (screen_rect.centerx - label1.get_width()/2, screen_rect.centery - 25))
            screen.blit(label2, (screen_rect.centerx - label2.get_width()/2, screen_rect.centery + 50))

    def over_screen(self):
        screen_rect = screen.get_rect()

        label1 = self.big_font.render(f"GAME OVER", 1, (255, 255, 255))
        label2 = self.small_font.render(f"Press SPACE to Continue", 1, (255, 255, 255))

        screen.blit(label1, (screen_rect.centerx - label1.get_width()/2, screen_rect.centery - 25))
        screen.blit(label2, (screen_rect.centerx - label2.get_width()/2, screen_rect.centery + 50))

    def end_screen(self):
        screen_rect = screen.get_rect()

        label1 = self.big_font.render(f"CONGRATULATIONS", 1, (255, 255, 255))
        label2 = self.small_font.render(f"Thanks For Playing RPG GO!", 1, (255, 255, 255))

        screen.blit(label1, (screen_rect.centerx - label1.get_width()/2, screen_rect.centery - 25))
        screen.blit(label2, (screen_rect.centerx - label2.get_width()/2, screen_rect.centery + 50))

    def run(self):
        # controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == BATTLE_STATE:
                self.battle.battle_controls(event)
            else:
                self.game_controls(event)

        # game states
        if self.state == START_STATE:
            # overlay
            self.overlay.update(self.loop)
            self.overlay.show(screen)

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

            # overlay
            self.overlay.update(self.loop)
            self.overlay.show(screen)

        elif self.state == GAME_OVER_STATE:
            # overlay
            self.overlay.update(self.loop)
            self.overlay.show(screen)

            self.over_screen()

        elif self.state == END_STATE:
            # overlay
            self.overlay.update(self.loop)
            self.overlay.show(screen)
            
            # show credits
            self.end_screen()
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
                if self.can_spawn() and self.loop % self.item_timer == 0:
                    self.spawn_component("item")  

                if self.state == LEVEL_STATE:
                    # increase speed
                    if self.loop % 1000 == 0:
                        self.speed += 0.25

                    # boss timer
                    if self.distance >= self.boss_distance:
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
                if self.can_spawn():
                    self.spawn_component()

                for component in self.components:
                    # remove obstacle if off screen
                    if component.x < -50:
                        self.components.remove(component)
                    else:
                        component.update(-self.speed, self.loop)
                        component.show(screen)
                        self.collision(self.player, component)

                # boss
                if self.boss:
                    self.boss.update(self)

                    if self.state != END_LEVEL_STATE:
                        self.boss.show(screen)
                        self.collision(self.player, self.boss)

                        # boss shot
                        for enemy_shot in self.enemy_shots:
                            enemy_shot.update(self.loop)
                            enemy_shot.show(screen)
                            self.collision(self.player, enemy_shot)
                
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
                    if self.boss:
                        self.collision(self.boss, player_shot)

            # bgm
            self.bgm.update(self)

            # overlay
            self.overlay.update(self.loop)
            self.overlay.show(screen)

            # score
            self.score.update(self)
            self.score.show(self, screen)

            # vfx
            for vfx in self.vfxs:
                if vfx.is_complete():
                    self.vfxs.remove(vfx)
                else:
                    vfx.update(self.loop)
                    vfx.show(screen)