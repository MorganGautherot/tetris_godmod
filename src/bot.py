import numpy as np
from src.config import *
import copy
import time, random

def random_bot(tetris):
    """Make a random action for the tetrominoes"""
    choice = np.random.randint(4)

    if choice == 0:
        tetris.move_left(tetris.current_tetromino, tetris.matrix)
    elif choice == 1:
        tetris.move_right(tetris.current_tetromino, tetris.matrix)
    elif choice == 2:
        tetris.rotation(tetris.current_tetromino, tetris.matrix)
    elif choice == 3:
        tetris.move_down(tetris.current_tetromino, tetris.matrix)

def count_hole_number(game_matrix:dict):
    """ 
    Count the nuber of hole in the tetris matrix. 
    A hole is an empty space cover by a tetrominoes
    """
    count_hole = 0
    number_hole = 0
    for width in range(MATRIX_WIDTH):

        number_hole = 0
        for height in range(MATRIX_HEIGHT-1, -1, -1):
            if game_matrix[height, width] is None:

                number_hole +=1
            if not(game_matrix[height, width] is None):
                count_hole += number_hole
                number_hole = 0

    return count_hole

def count_total_height(game_matrix:dict):
    total_height = 0
    for width in range(MATRIX_WIDTH):
        for height in range(MATRIX_HEIGHT):
            if not(game_matrix[height, width] is None) and isinstance(game_matrix[height, width][0], str) :
                total_height += MATRIX_HEIGHT-height
                break
    return total_height

def custom_metric(game_matrix:dict):
    number_hole = count_hole_number(game_matrix)
    total_height = count_total_height(game_matrix)

    return number_hole

def lowest_point(tetris, shape, position):
    # Starting position of the tetromino
    posY, posX = position

    # Find the lowest point possible for the tetromino 
    while tetris.blend(shape=shape, position=(posY, posX)):
        posY += 1   
        
    # Get the position of the lowest position for the shape
    # at a certain width
    position = (posY - 1, posX)  

    return position


def move_estimation(tetris, cost_function:callable)->tuple:
    """ 
    Try every posssible move and return the best roation and movement of the tetrominoes
    """
    best_position = list()
    best_rotation = list()
    minimum_cost = np.inf
    possible_rotation = 4

    current_tetromino_copy = copy.deepcopy(tetris.current_tetromino)

    # Try every rotation
    for rotation in range(1, possible_rotation+1): 

        tetris.rotation(current_tetromino_copy, tetris.matrix)

        # For every rotation try every x position
        for width in range(0, 1+MATRIX_WIDTH):   
            
            # start at the highest point and try every position in the x axis
            posY, posX = current_tetromino_copy.tetromino_position
            current_tetromino_copy.tetromino_position = (0, width)

            if tetris.fits_in_matrix(current_tetromino_copy.tetromino_position,
                              current_tetromino_copy.tetromino_shape,
                              tetris.matrix):

                futur_position, rotated_shape = tetris.last_valid_position(current_tetromino_copy, 
                                                                        tetris.matrix)
                current_tetromino_copy.tetromino_position = futur_position

                matrix_and_tetromino = tetris.add_tetromino_to_matrix(current_tetromino_copy, 
                                                                    tetris.matrix)

                position_cost = cost_function(matrix_and_tetromino) 

                time.sleep(0.2)
                print(futur_position)
                print(position_cost)
                tetris.tetris_window.redraw(tetris.tetris_window.screen, 
                                    matrix_and_tetromino,
                                    tetris.next_tetromino)

                # If the cost function is below the minimum cost
                if position_cost < minimum_cost:
                    best_position = list([futur_position])
                    best_rotation = list([rotation])
                    minimum_cost = position_cost

                # Add the move with other move at the same cost
                elif position_cost == minimum_cost:
                    best_position.append(futur_position)
                    best_rotation.append(rotation)

    # Take only one rotation or position from the possible move
    best_position = random.choice(best_position)
    best_rotation = random.choice(best_rotation)

    return best_position, best_rotation, minimum_cost


def system_expert(tetris):
    """
    place the tetrominoes minimizing the hole
    """

    (best_pos_y, best_pos_x), best_rotation, minimum_cost = move_estimation(tetris, custom_metric)

    posY, posX = tetris.current_tetromino.tetromino_position

    #for rotate in range(best_rotation):
    #    tetris.rotation(tetris.current_tetromino, tetris.matrix)
#
    #if best_pos_x > posX :
    #    for _ in range(best_pos_x-posX):
    #        tetris.move_right(tetris.current_tetromino, tetris.matrix)
#
    #elif best_pos_x < posX :
    #    for _ in range(posX-best_pos_x):
    #        tetris.move_left(tetris.current_tetromino, tetris.matrix)


    time.sleep(1)


    #tetris.hard_drop(tetris.current_tetromino, tetris.matrix)