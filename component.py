import pygame, os, math

class Component:
    def __init__(self, settings, screen_width, screen_height):
        # set surfaces
        self.settings = settings
        self.set_obstacle_surface(screen_width, screen_height)
        self.set_enemy_surface()
        self.set_item_surface(screen_width)

    def create_obstacle(self, x):
        new_obstacle = Obstacle(self.obstacle_surface, x, self.obstacle_y)
        return new_obstacle

    def create_enemy(self, x, y):
        new_enemy = Enemy_Field(self.enemy_surfaces, x, y)
        return new_enemy

    def create_item(self, x, screen_height):
        new_item = Item(self.item_surface, x, screen_height)
        return new_item

    def set_obstacle_surface(self, screen_width, screen_height):
        path = self.settings.get_level_setting("obstacle")
        image = pygame.image.load(path).convert_alpha()
        size = (round(screen_width/18), round(screen_height/4))
        self.obstacle_y = round(screen_height/1.75)
        self.obstacle_surface = pygame.transform.scale(image, size)

    def set_enemy_surface(self):
        enemy_run_paths = self.settings.get_enemy_setting("enemy_run")
        self.enemy_surfaces = []
        for path in enemy_run_paths:
            image = pygame.image.load(path).convert_alpha()
            self.enemy_surfaces.append(pygame.transform.scale2x(image))

    def set_item_surface(self, screen_width):
        path = self.settings.get_level_setting("item")
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
    
    def update(self, dx, loop):
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
    
    def update(self, dx, loop):
        self.x += dx
        self.rect.x = self.x

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def set_rect(self):
        self.rect = pygame.Rect(
            self.x, self.y, self.surface.get_width(), self.surface.get_height())

class Enemy_Field:
    def __init__(self, surfaces, x, y):
        self.x = x
        self.y = y
        self.surface_num = 0
        self.surfaces = surfaces
        self.surface = self.surfaces[0]
        self.set_rect()
    
    def update(self, dx, loop):
        self.x += dx
        self.rect.x = self.x
        if loop % 9 == 0:
            self.surface_num = (self.surface_num + 1) % 3
            self.surface = self.surfaces[self.surface_num]

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())