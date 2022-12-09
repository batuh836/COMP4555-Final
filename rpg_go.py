import pygame
from game import *

# pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('RPG GO!')

def main():
    #objects
    game = Game()
    clock = pygame.time.Clock()

    while True:
        game.run()
        clock.tick(60)
        pygame.display.update()

main()