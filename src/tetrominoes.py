from __future__ import print_function
from collections import namedtuple
import random

X, O = 'X', None
Tetromino = namedtuple("Tetrimino", "color shape")

tetrominoes_dict = {
    "long": Tetromino(color="blue",
                      shape=((O,O,O,O),
                             (X,X,X,X),
                             (O,O,O,O),
                             (O,O,O,O))),
    "square": Tetromino(color="yellow",
                        shape=((X,X),
                               (X,X))),
    "hat": Tetromino(color="pink",
                     shape=((O,X,O),
                            (X,X,X),
                            (O,O,O))),
    "right_snake": Tetromino(color="green",
                             shape=((O,X,X),
                                    (X,X,O),
                                    (O,O,O))),
    "left_snake": Tetromino(color="red",
                            shape=((X,X,O),
                                   (O,X,X),
                                   (O,O,O))),
    "left_gun": Tetromino(color="cyan",
                          shape=((X,O,O),
                                 (X,X,X),
                                 (O,O,O))),
    "right_gun": Tetromino(color="orange",
                           shape=((O,O,X),
                                  (X,X,X),
                                  (O,O,O)))
}
tetrominoes_list = list(tetrominoes_dict.keys())

class Tetrominoes():

    def __init__(self)->None:
        """Initialization of a tetrominoes"""
        self.rotation = 0
        self.tetromino_name = random.choice(tetrominoes_list)
        self.tetromino_shape = tetrominoes_dict[self.tetromino_name].shape
        self.tetromino_color = tetrominoes_dict[self.tetromino_name].color
        self.tetromino_position = (
            (2, 4) if len(self.tetromino_shape) == 2 else (2, 3)
        )

    def rotate(self,shape, times=1):
        """ Rotate a shape to the right """
        self.rotation = (self.rotation + times) % 4
        return shape if times == 0 else self.rotate(tuple(zip(*shape[::-1])), times-1)

    def shape_str(self):
        """ Return a string of a shape in human readable form """
        return '\n'.join(''.join(map({'X': 'X', None: 'O'}.get, line))
                        for line in self.tetromino_shape)

    def shape(self,shape):
        """ Print a shape in human readable form """
        print(self.shape_str(shape))

    def move_right(self)->None:
        """Change the position of the tetromino"""
        posY, posX = self.tetromino_position
        self.tetromino_position = posY, posX+1

    def move_left(self)->None:
        """Change the position of the tetromino"""
        posY, posX = self.tetromino_position
        self.tetromino_position = posY, posX-1

    def move_down(self)->None:
        """Change the position of the tetromino"""
        posY, posX = self.tetromino_position
        self.tetromino_position = posY+1, posX

