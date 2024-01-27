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

#def first_test():
#    """
#    Count number of hole in game board matrix.
#    In this test there is no hole
#    """
#    random.seed(7)
#    tetris_game = Tetris(display=True)
#
#    bot = DeepBot(tetris_game, 
#                   'artefacts/trained_model.hdf5')
#    
#    bot.move_tetromino(rotation=0, column=0)
#  
#    print( tetris_game.game_board_matrix[(18, 3)] )
#    print( tetris_game.game_board_matrix[(19, 4)] )
#    print( tetris_game.game_board_matrix[(18, 4)] )
#    print( tetris_game.game_board_matrix[(17, 4)] ) 
#    print( tetris_game.game_board_matrix[(18, 3)] == 'pink')
#    print( tetris_game.game_board_matrix[(19, 4)] == 'pink')
#    print( tetris_game.game_board_matrix[(18, 4)] == 'pink')
#    print( tetris_game.game_board_matrix[(17, 4)] == 'pink')
#
#
#
#first_test()


def test_add_tetromino_to_game_board_matrix():
    """
    Test the append of tetromino to the game board matrix
    """
    # Right_snake 
    random.seed(12)
    tetris_game = Tetris(take_picture = True, 
                    training_id=0,
                    display=False)

    list_of_coordonates = [
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (18, 2),
        (18, 3),
        (18, 4),
        (19, 4),
        (19, 5),
        (18, 8),
        (18, 9),
        (19, 8),
        (19, 9),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
    ]

    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "pink"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "red"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "yellow"

    matrix_and_tetromino = tetris_game.add_tetromino_to_game_board_matrix(tetris_game.current_tetromino, 
                                                        tetris_game.game_board_matrix)

    tetris_game.data_creation.game_board_to_image(tetris_game)
    
test_add_tetromino_to_game_board_matrix()

def test_add_tetromino_to_game_board_matrix():
    """
    Test the append of tetromino to the game board matrix
    """
    # Left_snake 
    random.seed(5)
    tetris_game = Tetris(take_picture = True, 
                    training_id=0,
                    display=False)

    list_of_coordonates = [
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (18, 2),
        (18, 3),
        (18, 4),
        (19, 4),
        (19, 5),
        (18, 8),
        (18, 9),
        (19, 8),
        (19, 9),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
    ]

    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "pink"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "red"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "yellow"

    matrix_and_tetromino = tetris_game.add_tetromino_to_game_board_matrix(tetris_game.current_tetromino, 
                                                        tetris_game.game_board_matrix)

    tetris_game.data_creation.game_board_to_image(tetris_game)
    
test_add_tetromino_to_game_board_matrix()

def test_add_tetromino_to_game_board_matrix():
    """
    Test the append of tetromino to the game board matrix
    """
    # Right gun
    random.seed(111)
    tetris_game = Tetris(take_picture = True, 
                    training_id=0,
                    display=False)

    list_of_coordonates = [
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (18, 2),
        (18, 3),
        (18, 4),
        (19, 4),
        (19, 5),
        (18, 8),
        (18, 9),
        (19, 8),
        (19, 9),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
    ]

    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "pink"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "red"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "yellow"

    matrix_and_tetromino = tetris_game.add_tetromino_to_game_board_matrix(tetris_game.current_tetromino, 
                                                        tetris_game.game_board_matrix)

    tetris_game.data_creation.game_board_to_image(tetris_game)
    
test_add_tetromino_to_game_board_matrix()

def test_add_tetromino_to_game_board_matrix():
    """
    Test the append of tetromino to the game board matrix
    """
    # Left gun
    random.seed(19)
    tetris_game = Tetris(take_picture = True, 
                    training_id=0,
                    display=False)

    list_of_coordonates = [
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (18, 2),
        (18, 3),
        (18, 4),
        (19, 4),
        (19, 5),
        (18, 8),
        (18, 9),
        (19, 8),
        (19, 9),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
    ]

    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "pink"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "red"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "yellow"

    matrix_and_tetromino = tetris_game.add_tetromino_to_game_board_matrix(tetris_game.current_tetromino, 
                                                        tetris_game.game_board_matrix)

    tetris_game.data_creation.game_board_to_image(tetris_game)
    
test_add_tetromino_to_game_board_matrix()

def test_add_tetromino_to_game_board_matrix():
    """
    Test the append of tetromino to the game board matrix
    """
    # square
    random.seed(1)
    tetris_game = Tetris(take_picture = True, 
                    training_id=0,
                    display=False)

    list_of_coordonates = [
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (18, 2),
        (18, 3),
        (18, 4),
        (19, 4),
        (19, 5),
        (18, 8),
        (18, 9),
        (19, 8),
        (19, 9),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
    ]

    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "pink"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "red"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "yellow"

    matrix_and_tetromino = tetris_game.add_tetromino_to_game_board_matrix(tetris_game.current_tetromino, 
                                                        tetris_game.game_board_matrix)

    tetris_game.data_creation.game_board_to_image(tetris_game)
    
test_add_tetromino_to_game_board_matrix()


def test_add_tetromino_to_game_board_matrix():
    """
    Test the append of tetromino to the game board matrix
    """
    # hate
    random.seed(7)
    tetris_game = Tetris(take_picture = True, 
                    training_id=0,
                    display=False)

    list_of_coordonates = [
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (18, 2),
        (18, 3),
        (18, 4),
        (19, 4),
        (19, 5),
        (18, 8),
        (18, 9),
        (19, 8),
        (19, 9),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
    ]

    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "pink"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "red"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "yellow"

    matrix_and_tetromino = tetris_game.add_tetromino_to_game_board_matrix(tetris_game.current_tetromino, 
                                                        tetris_game.game_board_matrix)

    tetris_game.data_creation.game_board_to_image(tetris_game)
    
test_add_tetromino_to_game_board_matrix()

def test_add_tetromino_to_game_board_matrix():
    """
    Test the append of tetromino to the game board matrix
    """
    # long
    random.seed(123)
    tetris_game = Tetris(take_picture = True, 
                    training_id=0,
                    display=False)

    list_of_coordonates = [
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (18, 2),
        (18, 3),
        (18, 4),
        (19, 4),
        (19, 5),
        (18, 8),
        (18, 9),
        (19, 8),
        (19, 9),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
    ]

    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "pink"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "red"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "yellow"

    matrix_and_tetromino = tetris_game.add_tetromino_to_game_board_matrix(tetris_game.current_tetromino, 
                                                        tetris_game.game_board_matrix)

    tetris_game.data_creation.game_board_to_image(tetris_game)
    
test_add_tetromino_to_game_board_matrix()