import cv2
import os
import numpy as np
from scraping.scraping import transform_image_into_matrix, transform_next_tetromino_to_matrix, detect_tetromino, determined_is_tetromino_start

def test_transform_next_tetromino_to_matrix():
    """
    Test the function transform_next_tetromino_to_matrix
    """

    path_right_snake = 'tests/data/frame167.jpg'
    right_snake_image = cv2.imread(path_right_snake)
    next_tetromino_matrix = transform_next_tetromino_to_matrix(right_snake_image)
    print(next_tetromino_matrix)
    assert np.array_equal(next_tetromino_matrix, [[0, 0, 255, 255, 0],
                                    [0, 255, 255, 0, 0]])
    
    path_left_snake = 'tests/data/frame289.jpg'
    left_snake_image = cv2.imread(path_left_snake)
    next_tetromino_matrix = transform_next_tetromino_to_matrix(left_snake_image)
    assert np.array_equal(next_tetromino_matrix, [[0, 255, 255, 0, 0],
                                    [0, 0, 255, 255, 0]])

    path_right_gun = 'tests/data/frame98.jpg' 
    right_gun_image = cv2.imread(path_right_gun)

    next_tetromino_matrix = transform_next_tetromino_to_matrix(right_gun_image)

    assert np.array_equal(next_tetromino_matrix, [[0, 255, 255, 255, 0],
                                    [0, 255, 0, 0, 0]])

    path_left_gun = 'tests/data/frame67.jpg'
    left_gun_image = cv2.imread(path_left_gun)

    next_tetromino_matrix = transform_next_tetromino_to_matrix(left_gun_image)
    assert np.array_equal(next_tetromino_matrix, [[0, 255, 255, 255, 0],
                                    [0, 0, 0, 255, 0]])

    path_square = 'tests/data/frame347.jpg'
    square_image = cv2.imread(path_square)

    next_tetromino_matrix = transform_next_tetromino_to_matrix(square_image)
    assert np.array_equal(next_tetromino_matrix, [[0, 255, 255, 255, 0],
                                    [0, 255, 255, 255, 0]])

    path_hat = 'tests/data/frame0.jpg'
    hat_image = cv2.imread(path_hat)

    next_tetromino_matrix = transform_next_tetromino_to_matrix(hat_image)
    assert np.array_equal(next_tetromino_matrix, [[0, 255, 255, 255, 0],
                                    [0, 0, 255, 0, 0]])

    path_long = 'tests/data/frame35.jpg' 
    long_image = cv2.imread(path_long)

    next_tetromino_matrix = transform_next_tetromino_to_matrix(long_image)
    assert np.array_equal(next_tetromino_matrix, [[255, 255, 255, 255, 255],
                                    [255, 255, 255, 255, 255]])
    
def test_detect_tetromino():
    """
    Test the function detect_tetromino
    """

    path_right_snake = 'tests/data/frame167.jpg'
    right_snake_image = cv2.imread(path_right_snake)
    next_tetromino_matrix = transform_next_tetromino_to_matrix(right_snake_image)
    tetromino_name = detect_tetromino(next_tetromino_matrix)
    assert tetromino_name == "right_snake"
    
    path_left_snake = 'tests/data/frame289.jpg'
    left_snake_image = cv2.imread(path_left_snake)
    next_tetromino_matrix = transform_next_tetromino_to_matrix(left_snake_image)
    tetromino_name = detect_tetromino(next_tetromino_matrix)
    assert tetromino_name == "left_snake"

    path_right_gun = 'tests/data/frame98.jpg' 
    right_gun_image = cv2.imread(path_right_gun)
    next_tetromino_matrix = transform_next_tetromino_to_matrix(right_gun_image)
    tetromino_name = detect_tetromino(next_tetromino_matrix)
    assert tetromino_name == "right_gun"

    path_left_gun = 'tests/data/frame67.jpg'
    left_gun_image = cv2.imread(path_left_gun)
    next_tetromino_matrix = transform_next_tetromino_to_matrix(left_gun_image)
    tetromino_name = detect_tetromino(next_tetromino_matrix)
    assert tetromino_name == "left_gun"

    path_square = 'tests/data/frame347.jpg'
    square_image = cv2.imread(path_square)
    next_tetromino_matrix = transform_next_tetromino_to_matrix(square_image)
    tetromino_name = detect_tetromino(next_tetromino_matrix)
    assert tetromino_name == "square"

    path_hat = 'tests/data/frame0.jpg'
    hat_image = cv2.imread(path_hat)
    next_tetromino_matrix = transform_next_tetromino_to_matrix(hat_image)
    tetromino_name = detect_tetromino(next_tetromino_matrix)
    assert tetromino_name == "hat"

    path_long = 'tests/data/frame35.jpg' 
    long_image = cv2.imread(path_long)
    next_tetromino_matrix = transform_next_tetromino_to_matrix(long_image)
    tetromino_name = detect_tetromino(next_tetromino_matrix)
    assert tetromino_name == "long"

def test_determined_is_tetromino_start():
    ''' 
    Test function determined_is_tetromino_start
    '''

    is_tetromino_path = 'tests/data/frame35.jpg' 
    is_tetromono = cv2.imread(is_tetromino_path)
    game_board_matrix = transform_image_into_matrix(is_tetromono)
    assert determined_is_tetromino_start(game_board_matrix) == True


    is_no_tetromino_path = 'tests/data/frame53.jpg' 
    is_no_tetromino = cv2.imread(is_no_tetromino_path)
    game_board_matrix = transform_image_into_matrix(is_no_tetromino)
    assert determined_is_tetromino_start(game_board_matrix) == False