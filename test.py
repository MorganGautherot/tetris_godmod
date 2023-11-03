from src.game import Tetris
import src.config as config
from src.tetrominoes import Tetrominoes
import numpy as np
import random
from src.score import Score
from src.bot import RandomBot

#hate     random.seed(7)
#square     random.seed(1)
#left_gun     random.seed(19)
#right_gun      random.seed(111)
#left_snake     random.seed(5)
#right_snake     random.seed(12)
#long  random.seed(123)

def test_random_bot_play_rotation():
    """ 
    Test the initialization of the random bot
    """
    random.seed(19)
    tetris_game = Tetris(display=False) 

    bot = RandomBot(tetris_game)
    random.seed(28)
    bot.play()

    assert tetris_game.current_tetromino.tetromino_shape == ((None, 'X', 'X'), (None, 'X', None), (None, 'X', None))

def test_random_bot_play_right():
    """ 
    Test the initialization of the random bot
    """
    random.seed(19)
    tetris_game = Tetris(display=False) 

    print(tetris_game.current_tetromino.tetromino_shape)

    print(tetris_game.current_tetromino.tetromino_position)

    bot = RandomBot(tetris_game)
    np.random.seed(122)
    bot.play()

    print(tetris_game.current_tetromino.tetromino_shape)
    print(tetris_game.current_tetromino.tetromino_position)



test_random_bot_play_right()