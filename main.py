from src.train import Train
from src.env_constant import *
import pygame

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    Train().main(screen)
