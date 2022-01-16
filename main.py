import pygame
from config import SIZE


class Game:

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SIZE)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()


class Camera:
    pass


if __name__ == '__main__':
    Game()
