import pygame, os, math

class Player:
    def __init__(self, screen_width, screen_height):
        self.width = round(screen_width/15)
        self.height = self.width
        self.x = round(screen_width/60)
        self.y = round(screen_height/1.5)
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.color = (255, 255, 255)

        self.health = 10
        self.ground_height = round(screen_height/1.5)
        self.jump_time = -1.0
        self.jump_duration = 1.0
        self.jump_interval = 0.05
        self.jump_height = round(screen_height/2)
        self.on_ground = True
        self.jumping = False
        self.surface_num = 0
        self.surfaces = []

        self.set_surface()
        self.set_rect()
        self.set_sound()

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
        elif self.on_ground and loop % 6 == 0:
            self.surface_num = (self.surface_num + 1) % 4
            self.surface = self.surfaces[self.surface_num]

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def show_health(self, screen):
        health_bar = ""
        for _ in range(self.health):
            health_bar += "|"

        label = self.font.render(f"HP {health_bar}", 1, self.color)
        location = (10, screen.get_height() - label.get_height() - 10)
        screen.blit(label, location)

    def set_surface(self):
        for i in range(4):
            path = os.path.join(f'assets/images/player/player_0{i}.png')
            image = pygame.image.load(path).convert_alpha()
            self.surfaces.append(pygame.transform.scale(image, (self.width, self.height)))
        self.surface = self.surfaces[0]

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width*0.5, self.height*0.5)

    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)

    def is_alive(self):
        return self.health > 0
    
    def jump(self):
        self.sound.play()
        self.jump_time = -1.0
        self.jumping = True
        self.on_ground = False

    def stop(self):
        self.jumping = False
        self.on_ground = True