from src.game import Tetris
import src.config as config
from src.tetrominoes import Tetrominoes
import numpy as np
import random
from src.score import Score
from src.bot import RandomBot, ExpertBot

#hate     random.seed(7)
#square     random.seed(1)
#left_gun     random.seed(19)
#right_gun      random.seed(111)
#left_snake     random.seed(5)
#right_snake     random.seed(12)
#long  random.seed(123)

def test_compute_cost():
    """
    Count number of hole in game board matrix.
    In this test there is no hole
    """
    random.seed(12)
    tetris_game = Tetris(display=True)

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

    mat_mat = tetris_game.add_tetromino_to_game_board_matrix(tetris_game.current_tetromino,
                                                 tetris_game.game_board_matrix)

    print(cost)

    tetris_game.tetris_window.redraw(mat_mat,
                                tetris_game.next_tetromino)


    while True :
        True






test_compute_cost()