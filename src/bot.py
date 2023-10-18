import numpy as np
from src.game import Tetris
from src.config import *
from pygame import Rect, Surface
from src.tetrominoes import rotate

import time, random

def random_bot(tetris:Tetris):
    """Make a random action for the tetrominoes"""
    choice = np.random.randint(3)

    if choice == 0:
        tetris.movement_keys["left"] = 1
        tetris.movement_keys["left"] = 0
        tetris.movement_keys_timer = (-tetris.movement_keys_speed) * 2
    elif choice == 1:
        tetris.movement_keys["right"] = 1
        tetris.movement_keys["right"] = 0
        tetris.movement_keys_timer = (-tetris.movement_keys_speed) * 2
    elif choice == 2:
        tetris.request_rotation()

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


def move_estimation(tetris:Tetris, cost_function:callable)->tuple:
    """ 
    Try every posssible move and return the best roation and movement of the tetrominoes
    """
    best_position = list()
    best_rotation = list()
    minimum_cost = np.inf
    possible_rotation = 4

    # Try every rotation
    for rotation in range(1, possible_rotation+1): 

        # For every rotation try every x position
        for width in range(MATRIX_WIDTH+1):   
            # start at the highest point and try every position in the x axis
            acutal_position = (4, width)

            possible_rotation, new_position, rotate_shape = tetris.request_rotation(acutal_position, rotation)

            if possible_rotation:
                position = lowest_point(tetris, rotate_shape, new_position)

       
                # Add the tetromino at the matrix game
                with_tetromino = tetris.blend(shape=rotate_shape,
                                                position=position, 
                                                shadow=True) 

                # If it's possible to add the tetromino compute the cost 
                # adding it at this place 
                if with_tetromino :
                    position_cost = cost_function(with_tetromino)    
                    print(rotation)
                    print(position)
                    print(position_cost)
                    # If the cost function is below the minimum cost
                    if position_cost < minimum_cost:
                        best_position = list([position])
                        best_rotation = list([rotation])
                        minimum_cost = position_cost

                    # Add the move with other move at the same cost
                    elif position_cost == minimum_cost:
                        best_position.append(position)
                        best_rotation.append(rotation)

    # Take only one rotation or position from the possible move
    best_position = random.choice(best_position)
    best_rotation = random.choice(best_rotation)

    return best_position, best_rotation, minimum_cost


def system_expert(tetris:Tetris):
    """
    place the tetrominoes minimizing the hole
    """

    (best_pos_y, best_pos_x), best_rotation, minimum_cost = move_estimation(tetris, custom_metric)
    print('----------')
    print(minimum_cost)
    print('----------')
    posY, posX = tetris.tetromino_position

    for rotate in range(best_rotation):

        tetris.request_rotation(tetris.tetromino_position, 1)
    
    if best_pos_x > posX :
        for _ in range(best_pos_x-posX):
            tetris.request_movement('right')

    elif best_pos_x < posX :
        for _ in range(posX-best_pos_x):
            tetris.request_movement('left')

    time.sleep(0.5)


    tetris.hard_drop()