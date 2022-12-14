import pygame

class Overlay:
    def __init__(self, screen):
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.alpha = 255
        self.fading_in_out = False
        self.fading_in = False
        self.fading_out = False
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))

    def is_transitioning(self):
        return self.fading_in_out or self.fading_in or self.fading_out

    def transtion(self):
        self.fading_in_out = True
        self.fading_in = True

    def fade_in(self):
        self.fading_in = True

    def fade_out(self):
        self.fading_out = True

    def update(self, loop):
        if self.fading_in_out:
            if self.fading_in:
                if self.alpha < 255:
                    self.alpha += 5
                else:
                    self.fading_in = False
                    self.fading_out = True
            elif self.fading_out:
                if self.alpha > 0:
                    self.alpha -= 5
                else:
                    self.fading_in_out = False
                    self.fading_out = False
        elif self.fading_in:
            if self.alpha < 255:
                self.alpha += 5
            else:
                self.fading_in = False
        elif self.fading_out:
            if self.alpha > 0:
                self.alpha -= 5
            else:
                self.fading_out = False
        # update alpha
        self.surface.set_alpha(self.alpha)

    def show(self, screen):
        screen.blit(self.surface, (0, 0))