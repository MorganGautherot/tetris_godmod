from src.game import Tetris
from src.bot import deep_bot, ExpertBot


tetris = Tetris(take_picture = False)



bot = ExpertBot(tetris)


while True:

    # Time of the game
    #tetris.tetromino_falls_over_time()

    matrix_and_tetromino = tetris.add_tetromino_to_game_board_matrix(tetris.current_tetromino, 
                                                          tetris.game_board_matrix)
    
    tetris.tetris_window.redraw(matrix_and_tetromino,
                                tetris.next_tetromino)

    #random_bot(tetris)
    tetris.user_action()
    bot.play()
    #print(count_hole_number(tetris.matrix))
    #custom_metric(tetris.matrix)
    #system_expert(tetris)


