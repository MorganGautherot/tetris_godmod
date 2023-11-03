
from src.bot import RandomBot, ExpertBot
from src.game import Tetris
import random
import numpy as np

def test_initialization_random_bot():
    """ 
    Test the initialization of the random bot
    """

    tetris_game = Tetris(display=False) 

    bot = RandomBot(tetris_game)

    assert isinstance(bot.tetris, Tetris)


def test_random_bot_play_right():
    """ 
    Test the random bot to move right
    """
    random.seed(19)
    tetris_game = Tetris(display=False) 

    bot = RandomBot(tetris_game)
    np.random.seed(28)
    bot.play()

    assert tetris_game.current_tetromino.tetromino_position == (0, 4)

def test_random_bot_play_left():
    """ 
    Test the random bot to move left
    """
    random.seed(19)
    tetris_game = Tetris(display=False) 

    bot = RandomBot(tetris_game)
    np.random.seed(50)
    bot.play()

    assert tetris_game.current_tetromino.tetromino_position == (0, 2)

def test_random_bot_play_down():
    """ 
    Test the random bot to move down
    """
    random.seed(19)
    tetris_game = Tetris(display=False) 

    bot = RandomBot(tetris_game)
    np.random.seed(122)
    bot.play()

    assert tetris_game.current_tetromino.tetromino_position == (1, 3)

def test_random_bot_play_rotation():
    """ 
    Test the initialization of the random bot
    """
    random.seed(19)
    tetris_game = Tetris(display=False) 

    bot = RandomBot(tetris_game)
    np.random.seed(121)
    bot.play()

    assert tetris_game.current_tetromino.tetromino_shape == ((None, 'X', 'X'), (None, 'X', None), (None, 'X', None))

def test_initialization_expert_bot():
    """ 
    Test the initialization of the expert bot
    """

    tetris_game = Tetris(display=False) 

    bot = ExpertBot(tetris_game)

    assert isinstance(bot.tetris, Tetris)