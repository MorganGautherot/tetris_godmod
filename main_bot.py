from src.game import Tetris
from src.bot import DeepBot, ExpertBot
import random


best_line = 0
best_score = 0 
best_seed = 0


tetris = Tetris(take_picture = False,
                training_id=3,
                display=True,
                seed=1132)
bot = ExpertBot(tetris)

#bot = DeepBot(tetris)

while not(tetris.game_over):
    
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

print(tetris.tetris_score.score)
print(tetris.tetris_score.lines)



