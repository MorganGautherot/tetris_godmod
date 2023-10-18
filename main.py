from src.game import Tetris
from src.bot import random_bot, count_hole_number, system_expert
tetris = Tetris()

while True:

    # Time of the game
    #tetris.tetromino_falls_over_time()

    matrix_and_tetromino = tetris.add_tetromino_to_matrix(tetris.current_tetromino, 
                                                          tetris.matrix)
    
    tetris.tetris_window.redraw(tetris.tetris_window.screen, 
                                matrix_and_tetromino,
                                tetris.next_tetromino)
    
    #random_bot(tetris)
    tetris.user_action()
    #print(count_hole_number(tetris.matrix))
    system_expert(tetris)

