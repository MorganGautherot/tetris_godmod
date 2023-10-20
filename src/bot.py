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
    return total_height

def count_hole_line(game_matrix:dict):
    total_width = 0
    for height in range(MATRIX_HEIGHT):
        hole_in_line = 0
        for width in range(MATRIX_WIDTH):
            if not(game_matrix[height, width] is None) :
                hole_in_line += 1
                
        if hole_in_line>0:
            total_width += (MATRIX_WIDTH-hole_in_line)*(MATRIX_HEIGHT-height)
    return total_width    

def count_max_height(game_matrix:dict):
    max_height = 0
    for width in range(MATRIX_WIDTH):
        for height in range(MATRIX_HEIGHT):
            if not(game_matrix[height, width] is None) and isinstance(game_matrix[height, width][0], str) :
                if MATRIX_HEIGHT-height > max_height:
                    max_height = MATRIX_HEIGHT-height
                
    return max_height  

def count_min_height(game_matrix:dict):
    min_height = np.inf
    for width in range(MATRIX_WIDTH):
        for height in range(MATRIX_HEIGHT):
            if not(game_matrix[height, width] is None) and isinstance(game_matrix[height, width][0], str) :
                if MATRIX_HEIGHT-height < min_height:
                    min_height = MATRIX_HEIGHT-height
                
    return min_height  

def count_long_open_hole(game_matrix:dict):
    max_height = count_max_height(game_matrix)

    count_long_hole = 0
    for width in range(MATRIX_WIDTH):

        for height in range(MATRIX_HEIGHT):
            if not(game_matrix[height, width] is None) or MATRIX_HEIGHT-1==height:
                
                if max_height - (MATRIX_HEIGHT-height) >= 4 and MATRIX_HEIGHT-1==height:
        
                    count_long_hole += max_height - (MATRIX_HEIGHT-height-1)
                elif max_height - (MATRIX_HEIGHT-height) >= 4 :
                    count_long_hole += max_height - (MATRIX_HEIGHT-height)
                break         
                
    return count_long_hole 

def is_line(game_matrix:dict):
    is_a_line = 0
    for height in range(MATRIX_HEIGHT):
        nb_blocks = 0
        for width in range(MATRIX_WIDTH):
            
            if not(game_matrix[height, width] is None):
                nb_blocks+=1

        if nb_blocks==MATRIX_WIDTH:
            is_a_line = -200

                
    return is_a_line 

def custom_metric(game_matrix:dict):
    number_hole = count_hole_number(game_matrix)
    total_height = count_total_height(game_matrix)/20
    total_width = count_hole_line(game_matrix)/20
    max_height = count_max_height(game_matrix)
    min_height = count_min_height(game_matrix)
    long_hole = count_long_open_hole(game_matrix)
    line = is_line(game_matrix)

    #print(f'number_hole : {number_hole}')
    #print(f'total_height : {total_height}')
    #print(f'total_width : {total_width}')
    #print(f'max_height : {max_height}')
    #print(f'min_height : {min_height}')
    #print(f'long_hole : {long_hole}')
    #print(f'is_line : {line}')

    return number_hole + total_height + total_width + max_height - min_height + long_hole + line

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
        for width in range(-3, MATRIX_WIDTH):   
            
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

                #tetris.tetris_window.redraw(tetris.tetris_window.screen, 
                #                            matrix_and_tetromino,
                #                            tetris.next_tetromino)
                #time.sleep(0.5)

                # If the cost function is below the minimum cost
                if position_cost < minimum_cost:
                    best_position = list([futur_position])
                    best_shape = list([rotated_shape])
                    minimum_cost = position_cost

                # Add the move with other move at the same cost
                elif position_cost == minimum_cost:
                    best_position.append(futur_position)
                    best_shape.append(rotated_shape)

    # Take only one rotation or position from the possible move
    if len(best_position) > 1:
        best_id = random.randint(0, len(best_position)-1)

        best_position = best_position[best_id]
        best_shape = best_shape[best_id]
    else:
        best_position = best_position[0]
        best_shape = best_shape[0]

    return best_position, best_shape, minimum_cost


def double_move_estimation(tetris, cost_function:callable)->tuple:
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
        for width in range(-3, MATRIX_WIDTH):   
            
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

                next_tetromino_copy = copy.deepcopy(tetris.next_tetromino)

                # Try every rotation
                for double_rotation in range(1, possible_rotation+1): 

                    tetris.rotation(next_tetromino_copy, matrix_and_tetromino)

                    # For every rotation try every x position
                    for double_width in range(-3, MATRIX_WIDTH):  
                

                        # start at the highest point and try every position in the x axis
                        double_posY, double_posX = next_tetromino_copy.tetromino_position
                        next_tetromino_copy.tetromino_position = (0, double_width)

                        if tetris.fits_in_matrix(next_tetromino_copy.tetromino_position,
                                        next_tetromino_copy.tetromino_shape,
                                        matrix_and_tetromino):

                            double_futur_position, double_rotated_shape = tetris.last_valid_position(next_tetromino_copy, 
                                                                                    matrix_and_tetromino)
                            next_tetromino_copy.tetromino_position = double_futur_position

                            double_matrix_and_tetromino = tetris.add_tetromino_to_matrix(next_tetromino_copy, 
                                                                                matrix_and_tetromino)


                            position_cost = cost_function(double_matrix_and_tetromino)

                            # If the cost function is below the minimum cost
                            if position_cost < minimum_cost:
                                best_position = list([futur_position])
                                best_shape = list([rotated_shape])
                                minimum_cost = position_cost

                            # Add the move with other move at the same cost
                            elif position_cost == minimum_cost:
                                best_position.append(futur_position)
                                best_shape.append(rotated_shape)
#

                            position_cost = cost_function(matrix_and_tetromino)
                            
                            #tetris.tetris_window.redraw(tetris.tetris_window.screen, 
                            #                            matrix_and_tetromino,
                            #                            tetris.next_tetromino)
#

                            # If the cost function is below the minimum cost
                            if position_cost < minimum_cost:
                                best_position = list([futur_position])
                                best_shape = list([rotated_shape])
                                minimum_cost = position_cost

                            # Add the move with other move at the same cost
                            elif position_cost == minimum_cost:
                                best_position.append(futur_position)
                                best_shape.append(rotated_shape)

    # Take only one rotation or position from the possible move
    if len(best_position) > 1:
        best_id = random.randint(0, len(best_position)-1)

        best_position = best_position[best_id]
        best_shape = best_shape[best_id]
    else:
        best_position = best_position[0]
        best_shape = best_shape[0]

    return best_position, best_shape, minimum_cost


def system_expert(tetris):
    """
    place the tetrominoes minimizing the hole
    """

    (best_pos_y, best_pos_x), best_shape, minimum_cost = double_move_estimation(tetris, custom_metric)
    
    tetris.current_tetromino.tetromino_shape = best_shape
    tetris.current_tetromino.tetromino_position = (0, best_pos_x)

    tetris.hard_drop(tetris.current_tetromino, tetris.matrix)

    #time.sleep(0.01)

