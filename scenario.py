from src.game import Tetris
import src.config as config
from src.tetrominoes import Tetrominoes
import numpy as np
import random
from src.score import Score
from src.bot import RandomBot, ExpertBot, DeepBot
import time

#hate     random.seed(7)
#square     random.seed(1)
#left_gun     random.seed(19)
#right_gun      random.seed(111)
#left_snake     random.seed(5)
#right_snake     random.seed(12)
#long  random.seed(123)

def test_scenario_one():
    """
    Count number of hole in game board matrix.
    In this test there is no hole
    """
    random.seed(19)
    tetris_game = Tetris(display=True)


    bot = DeepBot(tetris=tetris_game, 
                  model_path='artefacts/overfitter_model.hdf5',
                  model_architecture='simple_model',
                  display=True)
    bot.play()
    print( tetris_game.game_board_matrix[(19, 4)] == 'cyan')
    print( tetris_game.game_board_matrix[(19, 5)] == 'cyan')
    print( tetris_game.game_board_matrix[(19, 6)] == 'cyan')
    print( tetris_game.game_board_matrix[(18, 4)] == 'cyan' ) 


def test_scenario_two():
    """
    Count number of hole in game board matrix.
    In this test there is no hole
    """
    random.seed(123)
    tetris_game = Tetris(display=True)

    list_of_coordonates = [(19, 4), (19, 5), (19, 6), (18, 4)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    bot = DeepBot(tetris=tetris_game,
                  model_path='artefacts/overfitter_model.hdf5',
                  model_architecture='simple_model',
                  display=True)
    bot.play()



def test_scenario_three():
    """
    Count number of hole in game board matrix.
    In this test there is no hole
    """
    random.seed(12)
    tetris_game = Tetris(display=True)

    list_of_coordonates = [(19, 0), (18, 0), (19, 1), (19, 2)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    list_of_coordonates = [(19, 6), (19, 7), (19, 8), (19, 9)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    list_of_coordonates = [(19, 4), (18, 4), (19, 5), (18, 5)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    bot = DeepBot(tetris=tetris_game,
                  model_path='artefacts/overfitter_model.hdf5',
                  model_architecture='simple_model',
                  display=True)
    bot.play()



test_scenario_one()
time.sleep(0.5)
test_scenario_two()
time.sleep(0.5)
test_scenario_three()
time.sleep(0.5)