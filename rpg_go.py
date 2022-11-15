import math
import sys
import pygame
import os
import random

WIDTH = 623
HEIGHT = 150

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('RPG GO!')

class Battle:
    def __init__(self):
        self.width = WIDTH*0.75
        self.height = HEIGHT*0.75
        self.set_texture()
        self.set_rect()
        self.set_sound()

    def start(self):
        self.show()

    def update(self, loop):
        self.set_texture()

    def show(self):
        screen.blit(self.texture, (0,0))

    def set_texture(self):
        path = os.path.join(f'assets/images/battle_bg.png')
        self.texture = pygame.image.load(path).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def set_rect(self):
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)

class Player:
    def __init__(self):
        self.width = 44.0
        self.height = 44.0
        self.x = 10.0
        self.y = 80.0
        self.ground_height = 80.0
        self.jump_time = -1.0
        self.jump_duration = 1.0
        self.jump_interval = 0.05
        self.jump_height = 75.0
        self.on_ground = True
        self.jumping = False
        self.texture_num = 0
        self.set_texture()
        self.set_rect()
        self.set_sound()
        self.show()

    def update(self, loop):
        #jumping
        if self.jumping:
            if self.jump_time <= self.jump_duration:
                #calculate jump values
                time_elapsed = self.jump_time/self.jump_duration
                jump_frame = -1 * math.pow(time_elapsed, 2) + 1

                #apply jump values to y
                self.y = self.ground_height - (jump_frame * self.jump_height)
                self.rect.y = self.y

                #increment jump time
                self.jump_time += self.jump_interval
            else: 
                self.stop()
        #walking 
        elif self.on_ground and loop % 4 == 0:
            self.texture_num = (self.texture_num + 1) % 3
            self.set_texture()

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join(f'assets/images/dino{self.texture_num}.png')
        self.texture = pygame.image.load(path).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width*0.75, self.height*0.75)

    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)

    def jump(self):
        self.sound.play()
        self.jump_time = -1.0
        self.jumping = True
        self.on_ground = False

    def stop(self):
        self.jumping = False
        self.on_ground = True

class Obstacle:
    def __init__(self):
        # cactus values
        self.cactus_width = 34
        self.cactus_height = 44
        self.cactus_y = 80
        self.set_cactus_texture()

        # bird values
        self.bird_width = 34
        self.bird_height = 24
        self.set_bird_texture()

    def create_cactus(self, x):
        new_cactus = Cactus(self.cactus_texture, x, self.cactus_y)
        return new_cactus

    def create_bird(self, x, y):
        new_bird = Bird(self.bird_texture, x, y)
        return new_bird

    def set_cactus_texture(self):
        path = os.path.join('assets/images/cactus.png')
        self.cactus_texture = pygame.image.load(path).convert_alpha()
        self.cactus_texture = pygame.transform.scale(
            self.cactus_texture, (self.cactus_width, self.cactus_height))

    def set_bird_texture(self):
        path = os.path.join('assets/images/bird.png')
        self.bird_texture = pygame.image.load(path).convert_alpha()
        self.bird_texture = pygame.transform.scale(
            self.bird_texture, (self.bird_width, self.bird_height))

class Cactus:
    def __init__(self, texture, x, y):
        self.texture = texture
        self.x = x
        self.y = y
        self.set_rect()
        self.show()
    
    def update(self, dx):
        self.x += dx
        self.rect.x = self.x

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_rect(self):
        self.rect = pygame.Rect(
            self.x, self.y, self.texture.get_width(), self.texture.get_height())

class Bird:
    def __init__(self, texture, x, y):
        self.x = x
        self.y = y
        self.texture = texture
        self.set_rect()
        self.show()
    
    def update(self, dx):
        self.x += dx
        self.rect.x = self.x

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.texture.get_width(), self.texture.get_height())

class Collision:
    def between(self, obj1, obj2):
        if obj1.rect.colliderect(obj2.rect):
            return True

class BG:
    def __init__(self, x):
        self.width = WIDTH
        self.height = HEIGHT
        self.x = x
        self.set_texture()
        self.show()

    def update(self, dx):
        self.x += dx
        if self.x <= -WIDTH:
            self.x = WIDTH

    def show(self):
        screen.blit(self.texture, (self.x, 0))

    def set_texture(self):
        path = os.path.join('assets/images/bg.png')
        self.texture = pygame.image.load(path).convert()
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

class Score:
    def __init__(self, hs):
        self.high_score = hs
        self.score = 0
        self.font = pygame.font.SysFont('monospace', 18)
        self.color = (0, 0, 0)
        self.set_sound()
        self.show()

    def update(self, loop):
        self.score = loop // 10
        self.check_score()
        self.check_sound()

    def check_score(self):
        if self.score >= self.high_score:
            self.high_score = self.score

    def set_sound(self):
        path = os.path.join('assets/sounds/point.wav')
        self.sound = pygame.mixer.Sound(path)

    def show(self):
        self.label = self.font.render(f"HI {self.high_score} {self.score}", 1, self.color)
        label_width = self.label.get_rect().width
        screen.blit(self.label, (WIDTH - label_width - 10, 10))

    def check_sound(self):
        if self.score % 100 == 0 and self.score != 0:
            self.sound.play()

class Game:
    def __init__(self, high_score = 0):
        self.bg = [BG(0), BG(WIDTH)]
        self.player = Player()
        self.obstacle = Obstacle()
        self.obstacles = []
        self.obstacle_dist = 84
        self.collision = Collision()
        self.score = Score(high_score)
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
        # obstacle_type = 1

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
                bg.show()
            
            #player
            player.update(loop)
            player.show()

            #obstacles
            if game.can_spawn(loop):
                game.spawn_obstacle()

            for obstacle in game.obstacles:
                obstacle.update(-game.speed)
                obstacle.show()

                #collision
                if game.collision.between(player, obstacle):
                    game.over()

            game.score.update(loop)
            game.score.show()

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