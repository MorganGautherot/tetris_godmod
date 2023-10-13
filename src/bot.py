import numpy as np
from src.game import Tetris
from src.env_constant import *
from pygame import Rect, Surface

def random_bot() -> str:
    """Make a random action for the tetrominoes"""
    choice = np.random.randint(3)

    if choice == 0:
        move = "left"
    elif choice == 1:
        move = "right"
    elif choice == 2:
        move = "rotation"

    return move

def minimize_hole(tetris:Tetris) -> str:
    """
    place the tetrominoes minimizing the hole
    """

    nb_hole = tetris.count_hole_number()
    possible_rotation = 4
    #for rotation in range(possible_rotation):
    for width in range(MATRIX_WIDTH):

        posY, posX = tetris.tetromino_position
        while tetris.blend(position=(posY, posX)):
            posY += 1

        position = (posY - 1, posX)
        print(position)
        with_tetromino = tetris.blend(shape=tetris.current_tetromino,
                    position=position, 
                    shadow=True)
        print(with_tetromino)


