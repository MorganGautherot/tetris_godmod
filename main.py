from src.game import Tetris
from src.bot import deep_bot, custom_metric, count_hole_line, random_bot, count_total_height, count_hole_number, system_expert


tetris = Tetris(take_picture = False)



bot = deep_bot()


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
    bot.play(tetris)
    #print(count_hole_number(tetris.matrix))
    #custom_metric(tetris.matrix)
    #system_expert(tetris)


