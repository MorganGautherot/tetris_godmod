from src.game import Tetris
from src.bot import DeepBot, ExpertBot
import random

best_line = 0
best_score = 0 
best_seed_lines = 0
best_seed_score = 0

display = False

for i in range(0, 10000):

    tetris = Tetris(take_picture = False, 
                    training_id=i,
                    display=display,
                    seed=i)
    bot = ExpertBot(tetris)

    #bot = DeepBot(tetris)

    while not(tetris.game_over):
        
        # Time of the game
        #tetris.tetromino_falls_over_time()
        #matrix_and_tetromino = tetris.add_tetromino_to_game_board_matrix(tetris.current_tetromino, 
        #                                                    tetris.game_board_matrix)
        ##tetris.tetris_window.redraw(matrix_and_tetromino,
        #                                tetris.next_tetromino)
        #random_bot(tetris)
        #tetris.user_action()

        bot.play()
        #print(count_hole_number(tetris.matrix))
        #custom_metric(tetris.matrix)
        #system_expert(tetris)

    #print(f'seed : {i}')
    #print(f'line : {tetris.tetris_score.lines}')
    #print(f'score : {tetris.tetris_score.score}')
#



    if best_line < tetris.tetris_score.lines:
        best_seed_lines = i
        best_line = tetris.tetris_score.lines
        print("--------------------------")
        print(f'lines : {best_line}')
        print(f'seed : {i}')

    if best_score < tetris.tetris_score.score:
        best_seed_score = i
        best_score = tetris.tetris_score.score
        print("--------------------------")
        print(f'scores : {best_score}')
        print(f'seed : {i}')

    del tetris
    del bot







