import pygame, os, math

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

    def show(self, screen):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join(f'assets/images/dino{self.texture_num}.png')
        self.texture = pygame.image.load(path).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width*0.6, self.height*0.6)

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

class Health:
    def __init__(self):
        self.health = 100