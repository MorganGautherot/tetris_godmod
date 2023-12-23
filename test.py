from src.game import Tetris
import src.config as config
from src.tetrominoes import Tetrominoes
import numpy as np
import random
from src.score import Score
from src.bot import RandomBot, ExpertBot, DeepBot
import time
import tensorflow as tf

#hate     random.seed(7)
#square     random.seed(1)
#left_gun     random.seed(19)
#right_gun      random.seed(111)
#left_snake     random.seed(5)
#right_snake     random.seed(12)
#long  random.seed(123)

def first_test():
    """
    Count number of hole in game board matrix.
    In this test there is no hole
    """
    random.seed(7)
    tetris_game = Tetris(display=True)

    bot = DeepBot(tetris_game, 
                   'artefacts/trained_model.hdf5')
    
    bot.move_tetromino(rotation=0, column=0)
  
    print( tetris_game.game_board_matrix[(18, 3)] )
    print( tetris_game.game_board_matrix[(19, 4)] )
    print( tetris_game.game_board_matrix[(18, 4)] )
    print( tetris_game.game_board_matrix[(17, 4)] ) 
    print( tetris_game.game_board_matrix[(18, 3)] == 'pink')
    print( tetris_game.game_board_matrix[(19, 4)] == 'pink')
    print( tetris_game.game_board_matrix[(18, 4)] == 'pink')
    print( tetris_game.game_board_matrix[(17, 4)] == 'pink')



first_test()
