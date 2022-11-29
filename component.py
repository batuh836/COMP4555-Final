import pygame, os, math

class Component:
    def __init__(self, screen_width, screen_height):
        # set surfaces
        self.set_obstacle_surface(screen_width, screen_height)
        self.set_enemy_surface(screen_width, screen_height)
        self.set_item_surface(screen_width)

    def create_obstacle(self, x):
        new_obstacle = Obstacle(self.obstacle_surface, x, self.obstacle_y)
        return new_obstacle

    def create_enemy(self, x, y):
        new_enemy = Enemy_Field(self.enemy_surface, x, y)
        return new_enemy

    def create_item(self, x, screen_height):
        new_item = Item(self.item_surface, x, screen_height)
        return new_item

    def set_obstacle_surface(self, screen_width, screen_height):
        path = os.path.join('assets/images/cactus.png')
        image = pygame.image.load(path).convert_alpha()
        size = (round(screen_width/18), round(screen_height/4))
        self.obstacle_y = round(screen_height/1.75)
        self.obstacle_surface = pygame.transform.scale(image, size)

    def set_enemy_surface(self, screen_width, screen_height):
        path = os.path.join('assets/images/bird.png')
        image = pygame.image.load(path).convert_alpha()
        size = (round(screen_width/18), round(screen_height/10))
        self.enemy_surface = pygame.transform.scale(image, size)

    def set_item_surface(self, screen_width):
        path = os.path.join('assets/images/components/potion.png')
        image = pygame.image.load(path).convert_alpha()
        size = (round(screen_width/18), round(screen_width/18))
        self.item_surface = pygame.transform.scale(image, size)

class Item:
    def __init__(self, surface, x, screen_height):
        self.surface = surface
        self.x = x
        self.y = round(screen_height/1.5)
        self.ground_height = round(screen_height*0.65)
        self.jump_time = -2.0
        self.jump_duration = 2.0
        self.jump_interval = 0.025
        self.jump_height = round(screen_height*0.65)
        self.set_rect()
    
    def update(self, dx):
        self.x += dx
        self.rect.x = self.x
        
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
            self.jump_time = -2

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def set_rect(self):
        self.rect = pygame.Rect(
            self.x, self.y, self.surface.get_width(), self.surface.get_height())

class Obstacle:
    def __init__(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y
        self.set_rect()
    
    def update(self, dx):
        self.x += dx
        self.rect.x = self.x

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def set_rect(self):
        self.rect = pygame.Rect(
            self.x, self.y, self.surface.get_width(), self.surface.get_height())

class Enemy_Field:
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.surface = surface
        self.set_rect()
    
    def update(self, dx):
        self.x += dx
        self.rect.x = self.x

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())