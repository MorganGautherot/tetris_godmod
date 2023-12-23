
from src.bot import RandomBot, ExpertBot, DeepBot
from src.game import Tetris
import random
import numpy as np

# Random bot

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

# Expert system bot

def test_initialization_expert_bot():
    """ 
    Test the initialization of the expert bot
    """

    tetris_game = Tetris(display=False) 

    bot = ExpertBot(tetris_game)

    assert isinstance(bot.tetris, Tetris)

def test_count_hole_number_three():
    """
    Count number of hole in game board matrix.
    In this test there is three holes
    """

    random.seed(12)
    tetris_game = Tetris(display=False)

    bot = ExpertBot(tetris_game)

    list_of_coordonates = [(16, 6), (17, 6), (18, 6), (19, 6),
                           (15, 6), (14, 6), (13, 6),(12, 6),
                           (11, 6), (16, 3), (17, 3), (18, 3),
                           (19, 3), (15, 3), (14, 3), (13, 3),
                           (12, 3), (17, 0)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[16]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[17]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (17, 3)

    tetris_game.current_tetromino.tetromino_shape = (tetris_game.current_tetromino.rotate(
            tetris_game.current_tetromino.tetromino_shape, 1
        )
    )

    matrix_and_tetromino = tetris_game.add_tetromino_to_game_board_matrix(tetris_game.current_tetromino, 
                                                          tetris_game.game_board_matrix)

    assert bot.count_hole_number(matrix_and_tetromino) == 3
def test_count_hole_number_zero():
    """
    Count number of hole in game board matrix.
    In this test there is no hole
    """

    random.seed(12)
    tetris_game = Tetris(display=False)

    bot = ExpertBot(tetris_game)

    list_of_coordonates = [(16, 6), (17, 6), (18, 6), (19, 6),
                           (15, 6), (14, 6), (13, 6),(12, 6),
                           (11, 6), (16, 3), (17, 3), (18, 3),
                           (19, 3), (15, 3), (14, 3), (13, 3),
                           (12, 3), (19, 0)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[16]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[17]] = "blue"


    assert bot.count_hole_number(tetris_game.game_board_matrix) == 0

def test_move_estimation():
    """
    test the compute the cost for every move of the current tetromino
    """
    random.seed(7)
    tetris_game = Tetris(display=False)

    bot = ExpertBot(tetris_game)

    list_of_coordonates = [(16, 6), (17, 6), (18, 6), (19, 6),
                           (15, 6), (14, 6), (13, 6),(12, 6),
                           (11, 6), (16, 3), (17, 3), (18, 3),
                           (19, 3), (15, 3), (14, 3), (13, 3),
                           (12, 3), (19, 0)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[16]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[17]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (0, 3)

    tetris_game.current_tetromino.tetromino_shape = (tetris_game.current_tetromino.rotate(
            tetris_game.current_tetromino.tetromino_shape, 1
        )
    )

    cost = bot.move_estimation(tetris_game.current_tetromino,
                               tetris_game.game_board_matrix,
                               bot.count_hole_number,
                               False)

    assert cost.shape == (34, 3)
    assert cost['cost'].min() == 0

def test_play():
    """
    Test the function play that place the tetromino to the best possible place
    """
    random.seed(12)
    tetris_game = Tetris(display=False)

    bot = ExpertBot(tetris_game)

    list_of_coordonates = [(19, 1), (19, 2), (19, 4), (18, 4),
                           (19, 5), (19, 6), (19, 7),(19, 8),
                           (18, 5), (18, 6), (18, 7), (18, 8)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (0, 3)

    bot.play()

    assert tetris_game.game_board_matrix[(19, 3)] == 'green'
    assert tetris_game.game_board_matrix[(18, 3)] == 'green'
    assert tetris_game.game_board_matrix[(18, 2)] == 'green'
    assert tetris_game.game_board_matrix[(17, 2)] == 'green'

def test_count_max_height():
    """
    Count the maximum height of the matrix
    """
    random.seed(12)
    tetris_game = Tetris(display=False)

    bot = ExpertBot(tetris_game)

    list_of_coordonates = [(19, 0), (18, 0), (17, 0), (16, 0),
                           (15, 0), (14, 0), (19, 8),(18, 8),
                           (17, 8), (16, 8), (15, 8), (14, 8),
                           (19, 5), (18, 5), (17, 5), (16, 5)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"


    cost = bot.count_max_height(tetris_game.game_board_matrix)

    assert cost == 6
def test_is_line_true():
    """
    Test the dection of line
    """
    random.seed(12)
    tetris_game = Tetris(display=False)

    bot = ExpertBot(tetris_game)

    list_of_coordonates = [(18, 0), (18, 1), (18, 2), (18, 3),
                           (18, 4), (18, 5), (18, 6),(18, 7),
                           (18, 8), (18, 9), (19, 0), (19, 1),
                           (19, 2), (19, 3), (19, 4), (19, 5)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"


    cost = bot.is_line(tetris_game.game_board_matrix)

    assert cost == -300

def test_is_line_false():
    """
    Test the dection of line
    """
    random.seed(12)
    tetris_game = Tetris(display=False)

    bot = ExpertBot(tetris_game)

    list_of_coordonates = [(18, 0), (18, 1), (18, 2), (18, 3),
                           (18, 4), (18, 5), (19, 6),(18, 7),
                           (18, 8), (18, 9), (19, 0), (19, 1),
                           (19, 2), (19, 3), (19, 4), (19, 5)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"


    cost = bot.is_line(tetris_game.game_board_matrix)

    assert cost == 0

def test_count_min_height():
    """
    Count the minimum number of height of the game matrix
    """
    random.seed(12)
    tetris_game = Tetris(display=False)

    bot = ExpertBot(tetris_game)

    list_of_coordonates = [(18, 0), (18, 1), (18, 2), (18, 3),
                           (18, 4), (18, 5), (19, 6),(18, 7),
                           (18, 8), (18, 9), (19, 0), (19, 1),
                           (19, 2), (19, 3), (19, 4), (19, 5)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"

    cost = bot.count_min_height(tetris_game.game_board_matrix)
    
    assert cost == 1

def test_count_hole_column():
    """
    Count number of hole column in the game matrix
    """
    random.seed(12)
    tetris_game = Tetris(display=False)

    bot = ExpertBot(tetris_game)

    list_of_coordonates = [(19, 1), (18, 1), (17, 1), (16, 1),
                           (19, 9), (18, 9), (17, 9), (16, 9),
                           (19, 7), (18, 7), (17, 7), (16, 7),
                           (15, 7), (15, 9), (16, 8), (19, 0)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (0, 3)

    cost = bot.count_hole_column(tetris_game.game_board_matrix)

    assert cost == 3

# Deep bot 

def test_create_matrix():
        """
        Test the function that map dict into np.array
        """
        random.seed(19)
        tetris_game = Tetris(display=False)

        list_of_coordonates = [
                (19, 0),
                (19, 1),
                (19, 2),
                (19, 3),
                (19, 4),
                (19, 5),
                (19, 6),
                (19, 7),
                (19, 8),
                (19, 9),
                (18, 9),
                (18, 8),
            ]
        tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
        tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
        tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
        tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

        tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
        tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
        tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
        tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

        tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
        tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
        tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
        tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

        bot = DeepBot(tetris_game, 
                    'artefacts/trained_model.hdf5',
                    display=False)
        
        matrix = bot.create_matrix(tetris_game.game_board_matrix)
        
        final_matrix = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 1., 1.],
                                [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]])


        assert matrix.shape == (1, 20, 10, 1)
        assert isinstance(matrix, np.ndarray)
        assert np.array_equal(matrix[0, :, :, 0], final_matrix)

def test_play():
    """
    Test the function that move tetromino in function of the game board situation
    """
    random.seed(7)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
            (19, 0),
            (19, 1),
            (19, 2),
            (19, 3),
            (19, 4),
            (19, 6),
            (19, 7),
            (19, 8),
            (19, 9),
            (18, 0),
            (18, 1),
            (18, 2),
            (18, 3),
            (18, 7),
            (18, 8),
            (18, 9),
        ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"

    bot = DeepBot(tetris_game, 
                   'artefacts/trained_model.hdf5',
                   display=False)
    
    bot.play()
    

    assert tetris_game.game_board_matrix[(17, 0)] == 'pink'
    assert tetris_game.game_board_matrix[(17, 1)] == 'pink'
    assert tetris_game.game_board_matrix[(17, 2)] == 'pink'
    assert tetris_game.game_board_matrix[(16, 1)] == 'pink'

def test_move_hat_no_rotation():
    """
    Count number of hole in game board matrix.
    In this test there is no hole
    """
    random.seed(7)
    tetris_game = Tetris(display=False)

    bot = DeepBot(tetris_game, 
                   'artefacts/trained_model.hdf5')
    
    bot.move_tetromino(rotation=0, column=3)
  

    assert tetris_game.game_board_matrix[(19, 3)] == 'pink'
    assert tetris_game.game_board_matrix[(19, 4)] == 'pink'
    assert tetris_game.game_board_matrix[(19, 5)] == 'pink'
    assert tetris_game.game_board_matrix[(18, 4)] == 'pink'

def test_move_hat_one_rotation():
    """
    Count number of hole in game board matrix.
    In this test there is no hole
    """
    random.seed(7)
    tetris_game = Tetris(display=False)

    bot = DeepBot(tetris_game, 
                   'artefacts/trained_model.hdf5')
    
    bot.move_tetromino(rotation=1, column=3)
  
    assert tetris_game.game_board_matrix[(19, 3)] == 'pink'
    assert tetris_game.game_board_matrix[(18, 3)] == 'pink'
    assert tetris_game.game_board_matrix[(17, 3)] == 'pink'
    assert tetris_game.game_board_matrix[(18, 4)] == 'pink'

def test_move_hat_two_rotation():
    """
    Count number of hole in game board matrix.
    In this test there is no hole
    """
    random.seed(7)
    tetris_game = Tetris(display=False)

    bot = DeepBot(tetris_game, 
                   'artefacts/trained_model.hdf5')
    
    bot.move_tetromino(rotation=2, column=3)
  

    assert tetris_game.game_board_matrix[(19, 4)] == 'pink'
    assert tetris_game.game_board_matrix[(18, 3)] == 'pink'
    assert tetris_game.game_board_matrix[(18, 4)] == 'pink'
    assert tetris_game.game_board_matrix[(18, 5)] == 'pink'

def test_move_hat_three_rotation():
    """
    Count number of hole in game board matrix.
    In this test there is no hole
    """
    random.seed(7)
    tetris_game = Tetris(display=False)

    bot = DeepBot(tetris_game, 
                   'artefacts/trained_model.hdf5')
    
    bot.move_tetromino(rotation=3, column=3)
  

    assert tetris_game.game_board_matrix[(18, 3)] == 'pink'
    assert tetris_game.game_board_matrix[(19, 4)] == 'pink'
    assert tetris_game.game_board_matrix[(18, 4)] == 'pink'
    assert tetris_game.game_board_matrix[(17, 4)] == 'pink'