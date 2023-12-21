from src.game import Tetris
from src.bot import deep_bot, ExpertBot



#bot = deep_bot()

display = False

for i in range(10000, 20000):
    tetris = Tetris(take_picture = True, 
                    training_id=i,
                    display=display)
    bot = ExpertBot(tetris)
    cmpt = 0
    tmp_score = 0
    while not(tetris.game_over) and cmpt < 1:

        # Time of the game
        #tetris.tetromino_falls_over_time()

        matrix_and_tetromino = tetris.add_tetromino_to_game_board_matrix(tetris.current_tetromino, 
                                                            tetris.game_board_matrix)
        if display:
            tetris.tetris_window.redraw(matrix_and_tetromino,
                                        tetris.next_tetromino)

        #random_bot(tetris)
        tetris.user_action()
        bot.play()
        #bot.play(tetris)
        #print(count_hole_number(tetris.matrix))
        #custom_metric(tetris.matrix)
        #system_expert(tetris)


        if tetris.tetris_score.score > tmp_score :
            tmp_score = tetris.tetris_score.score
            cmpt+=1
        print(cmpt)

print('quit')


