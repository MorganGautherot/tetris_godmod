import numpy as np
from src.config import *
import copy
import time, random
import tensorflow as tf

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



class deep_bot():

    def __init__(self):

        self.model = self.init_model()

    def base_model(self, inputs):

        x = tf.keras.layers.Conv2D(8, (3, 3), padding="same", activation='relu', input_shape=(20, 10, 1))(inputs)
        x = tf.keras.layers.MaxPooling2D((2, 2))(x)
        x = tf.keras.layers.Conv2D(16, (3, 3), padding="same", activation='relu')(x)
        x = tf.keras.layers.MaxPooling2D((2, 2))(x)
        x = tf.keras.layers.Conv2D(32, (3, 3), padding="same", activation='relu')(x)
        x = tf.keras.layers.MaxPooling2D((2, 2))(x)
        x = tf.keras.layers.Conv2D(64, (3, 3), padding="same", activation='relu')(x)
        x = tf.keras.layers.Flatten()(x)
        x = tf.keras.layers.Dense(64, activation='relu')(x)
        output = tf.keras.layers.Dense(units = '40', activation = 'softmax')(x)
        model = tf.keras.models.Model(inputs=inputs, outputs = output) 
        return model

    def init_model(self):
        inputs = tf.keras.layers.Input(shape=(20, 10, 1))
        model = self.base_model(inputs)
        model.load_weights('artefacts/trained_model.hdf5')
        return model


    def create_matrix(self, tetris):
        matrix = np.zeros((20, 10))

        for i in range(20):
            for j in range(10):
                if not(tetris.matrix[i, j] is None):
                    matrix[i, j]=1
        
        maitrix_shaped = np.expand_dims(matrix, axis=-1)

        return maitrix_shaped

    def no_whole(self, game_matrix):

      gamme_matrix_without_current_tetromino = game_matrix.copy()

      width, colmun, _ = gamme_matrix_without_current_tetromino.shape

      for col in np.arange(colmun):
        first_tetromino = np.argmax(gamme_matrix_without_current_tetromino[2:, col, :])

        gamme_matrix_without_current_tetromino[first_tetromino:, col, :]=1

      return gamme_matrix_without_current_tetromino

    def play(self, tetris):

        input_image = self.create_matrix(tetris)

        
        input_image = np.expand_dims(self.no_whole(input_image), axis=0)

        prediction = self.model.predict(input_image)

        column = np.argmax(prediction)%10
        rotation = int(np.floor(np.argmax(prediction)/10))

        print('-----')
        print(np.argmax(prediction))
        print(f'rotation : {rotation}')
        print(f'column : {column}')      

        self.move_tetromino(tetris, rotation, column)

    def move_tetromino(self, tetris, rotation, column):

        (posY, posX) = tetris.current_tetromino.tetromino_position

        for _ in range(rotation):
            
            tetris.rotation(tetris.current_tetromino, tetris.matrix)

            matrix_and_tetromino = tetris.add_tetromino_to_matrix(tetris.current_tetromino, 
                                                    tetris.matrix)
            tetris.tetris_window.redraw(tetris.tetris_window.screen, 
                                    matrix_and_tetromino,
                                    tetris.next_tetromino)
            time.sleep(1)


        binary_shape = np.where(np.array(tetris.current_tetromino.tetromino_shape)=='X', 1, 0)
        shape_in_box = np.sum(binary_shape, axis=0)

        for i in range(len(shape_in_box)):

            if shape_in_box[i]>0:
                column -= i
                break

        movement = column - posX

        if movement > 0:
            for _ in range(movement):

                tetris.move_right(tetris.current_tetromino, tetris.matrix)

                matrix_and_tetromino = tetris.add_tetromino_to_matrix(tetris.current_tetromino, 
                                                    tetris.matrix)
                tetris.tetris_window.redraw(tetris.tetris_window.screen, 
                                    matrix_and_tetromino,
                                    tetris.next_tetromino)
                time.sleep(1)
        elif movement < 0:
            for _ in range(-movement):

                tetris.move_left(tetris.current_tetromino, tetris.matrix)
                matrix_and_tetromino = tetris.add_tetromino_to_matrix(tetris.current_tetromino, 
                                                    tetris.matrix)
                tetris.tetris_window.redraw(tetris.tetris_window.screen, 
                                    matrix_and_tetromino,
                                    tetris.next_tetromino)
                time.sleep(1)

        time.sleep(1)
        tetris.hard_drop(tetris.current_tetromino, tetris.matrix)        