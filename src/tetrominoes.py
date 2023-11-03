from __future__ import print_function
from collections import namedtuple
import random

Tetromino = namedtuple("Tetrimino", "color shape")

tetrominoes_dict = {
    "long": Tetromino(
        color="blue", shape=((None, None, None, None),
                             ("X", "X", "X", "X"),
                             (None, None, None, None),
                             (None, None, None, None))),
    "square": Tetromino(color="yellow", shape=(("X", "X"),
                                               ("X", "X"))),
    "hat": Tetromino(color="pink", shape=((None, "X", None),
                                          ("X", "X", "X"),
                                          (None, None, None))),
    "right_snake": Tetromino(color="green", shape=((None, "X", "X"),
                                                   ("X", "X", None),
                                                   (None, None, None))),
    "left_snake": Tetromino(color="red", shape=(("X", "X", None),
                                                (None, "X", "X"),
                                                (None, None, None))),
    "left_gun": Tetromino(color="cyan", shape=(("X", None, None),
                                               ("X", "X", "X"),
                                               (None, None, None))),
    "right_gun": Tetromino(color="orange", shape=((None, None, "X"),
                                                  ("X", "X", "X"),
                                                  (None, None, None))),
}

tetrominoes_list = list(tetrominoes_dict.keys())


class Tetrominoes:
    def __init__(self) -> None:
        """
        Initialization of a tetrominoes
        """
        self.rotation = 0
        self.tetromino_name = random.choice(tetrominoes_list)
        self.tetromino_shape = tetrominoes_dict[self.tetromino_name].shape
        self.tetromino_color = tetrominoes_dict[self.tetromino_name].color
        self.tetromino_position = (0, 4) if len(self.tetromino_shape) == 2 else (0, 3)

    def rotate(self, shape: tuple, times: int = 1) -> tuple:
        """
        Rotate a shape to the right
        """
        self.rotation = (self.rotation + times) % 4
        return shape if times == 0 else self.rotate(tuple(zip(*shape[::-1])), times - 1)

    def move_right(self) -> None:
        """
        Change the position of the tetromino
        """
        posY, posX = self.tetromino_position
        self.tetromino_position = posY, posX + 1

    def move_left(self) -> None:
        """
        Change the position of the tetromino
        """
        posY, posX = self.tetromino_position
        self.tetromino_position = posY, posX - 1

    def move_down(self) -> None:
        """
        Change the position of the tetromino
        """
        posY, posX = self.tetromino_position
        self.tetromino_position = posY + 1, posX
