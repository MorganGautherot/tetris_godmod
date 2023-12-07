import numpy as np
import copy
import src.config as config
from src.tetrominoes import Tetrominoes
import time, random
import tensorflow as tf
from src.game import Tetris
import pandas as pd
import time

class RandomBot():

    def __init__(self, tetris:Tetris)->None:
        """
        Initialization of the random bot
        """
        self.tetris = tetris

    def play(self)->None:
        """
        Make a random action for the tetrominoes
        """
        choice = np.random.randint(4)

        if choice == 0:
            self.tetris.move_left()
        elif choice == 1:
            self.tetris.move_right()
        elif choice == 2:
            self.tetris.rotation()
        elif choice == 3:
            self.tetris.move_down()

class ExpertBot():

    def __init__(self, tetris:Tetris)->None:
        """
        Initialization of the expert bot
        """
        self.tetris = tetris

    def count_min_height(self, game_matrix:dict)->float:
        """
        Return the minimum height of the game matrix
        """
        min_height = np.inf
        for width in range(config.MATRIX_WIDTH):
            for height in range(config.MATRIX_HEIGHT):
                if not(game_matrix[height, width] is None) and isinstance(game_matrix[height, width][0], str) :
                    if config.MATRIX_HEIGHT-height < min_height:
                        min_height = config.MATRIX_HEIGHT-height
                    
        return min_height  
    

    def count_hole_column(self, game_matrix:dict, 
                          minimum_line:int=2)->float:
        """
        coutn the number of line hole column
        """
        count_long_hole = 0
        for width in range(config.MATRIX_WIDTH):
            row = 0
            for height in range(config.MATRIX_HEIGHT-1, -1, -1):
                
                if ((width-1) < 0 or not(game_matrix[height, width-1] is None)) and ((width+1) > 9 or not(game_matrix[height, width+1] is None)) and game_matrix[height, width] is None:
                    row +=1

                elif  not(game_matrix[height, width] is None):
                    row=0

            if row > minimum_line :
                count_long_hole += row
                    
        return count_long_hole 

    def count_max_height(self, game_matrix:dict)->float:
        """
        Return the max height of the game board matrix
        """
        max_height = 0
        for width in range(config.MATRIX_WIDTH):
            for height in range(config.MATRIX_HEIGHT):
                if not(game_matrix[height, width] is None) and isinstance(game_matrix[height, width][0], str) :
                    if config.MATRIX_HEIGHT-height > max_height:
                        max_height = config.MATRIX_HEIGHT-height
                    
        return max_height  
    
    def is_line(self, game_matrix:dict)->float:
        """
        Detect if there is a line in the game matrix
        """
        nb_line = 0
        for height in range(config.MATRIX_HEIGHT):
            nb_blocks = 0
            for width in range(config.MATRIX_WIDTH):
                
                if not(game_matrix[height, width] is None):
                    nb_blocks+=1

            if nb_blocks==config.MATRIX_WIDTH:
                nb_line += 1

                
        return np.where(nb_line==0, 0, -300 ** nb_line)

    def custom_metric(self, game_matrix:dict)->float:
        """
        Mix different cost function
        """
        nb_hole = self.count_hole_number(game_matrix)
        max_height = self.count_max_height(game_matrix)
        min_height = self.count_min_height(game_matrix)
        line = self.is_line(game_matrix)
        hole_colmun = self.count_hole_column(game_matrix)

        return nb_hole + max_height + line - min_height + hole_colmun

    def count_hole_number(self, game_matrix:dict)->float:
        """ 
        Count the number of hole in the tetris matrix. 
        A hole is an empty space cover by a tetrominoes
        """
        count_hole = 0
        number_hole = 0
        for width in range(config.MATRIX_WIDTH):

            number_hole = 0
            for height in range(config.MATRIX_HEIGHT-1, -1, -1):
                if game_matrix[height, width] is None:

                    number_hole +=1
                if not(game_matrix[height, width] is None):
                    count_hole += number_hole
                    number_hole = 0

        return count_hole

    def move_estimation(self, 
                        tetromino:Tetrominoes,
                        game_board_matrix:dict,
                        cost_function:callable,
                        recursivity_id:bool=True)->pd.DataFrame:
        """
        Estimation of the cost for every tetromino move possible
        """

        move_cost_dataframe = pd.DataFrame([], columns=('id_column', 
                                                        'id_rotation',
                                                        'cost'))
        if tetromino.tetromino_name in ['right_gun', 'left_gun', 'hat']:
            possible_rotation = 4
        elif tetromino.tetromino_name in ['long', 'right_snake', 'left_snake']:
            possible_rotation = 2
        else :
            possible_rotation = 1

        current_tetromino_copy = copy.deepcopy(tetromino)

        # Try every rotation
        for rotation in range(0, possible_rotation):

            if rotation > 0:
                new_shape = current_tetromino_copy.rotate(current_tetromino_copy.tetromino_shape)
                current_tetromino_copy.tetromino_shape = new_shape

            # For every rotation try every x position
            for width in range(-2, config.MATRIX_WIDTH):   
                
                # start at the highest point and try every position in the x axis
                current_tetromino_copy.tetromino_position = (0, width)

                if self.tetris.fits_in_game_board_matrix(current_tetromino_copy.tetromino_position,
                                                         current_tetromino_copy.tetromino_shape,
                                                         game_board_matrix):


                    last_position = self.tetris.last_valid_position(current_tetromino_copy,
                                                                    game_board_matrix)

                    current_tetromino_copy.tetromino_position = last_position

                    matrix_and_tetromino = self.tetris.add_tetromino_to_game_board_matrix(current_tetromino_copy, 
                                                                        game_board_matrix)
                    
                    if recursivity_id :
                        first_cost = cost_function(matrix_and_tetromino)
                        recursive_cost = self.move_estimation(self.tetris.next_tetromino,
                                                                   matrix_and_tetromino,
                                                                   self.custom_metric,
                                                                   recursivity_id=False)
                        position_cost = recursive_cost['cost'].min()*0.5 + first_cost
                    else :
                        position_cost = cost_function(matrix_and_tetromino)

                    #self.tetris.tetris_window.redraw(matrix_and_tetromino,
                    #                                 current_tetromino_copy)
                    #time.sleep(0.1)
   
                    new_line = pd.DataFrame([[width, 
                                              rotation,
                                              position_cost]], 
                                            columns=('id_column', 
                                                        'id_rotation',
                                                        'cost'))

                    move_cost_dataframe = pd.concat([move_cost_dataframe, new_line])

        return move_cost_dataframe

    def play(self)->None:
        """
        place the tetrominoes minimizing the hole
        """

        move_cost_dataframe = self.move_estimation(self.tetris.current_tetromino,
                                                   self.tetris.game_board_matrix,
                                                    self.custom_metric,
                                                    recursivity_id=True)

        minimum_move_cost_dataframe = move_cost_dataframe[move_cost_dataframe['cost']==move_cost_dataframe['cost'].min()]
        #print(minimum_move_cost_dataframe)
        next_position = minimum_move_cost_dataframe.sample(1)
        #print(next_position)

        new_shape = self.tetris.current_tetromino.rotate(self.tetris.current_tetromino.tetromino_shape,
                                                  times=next_position.loc[0, 'id_rotation'])
        self.tetris.current_tetromino.tetromino_shape = new_shape
   
        self.tetris.current_tetromino.tetromino_position = (0, next_position.loc[0, 'id_column'])

        self.tetris.hard_drop()

        #time.sleep(0.2)

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
                if not(tetris.game_board_matrix[i, j] is None):
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
            
            tetris.rotation()

            matrix_and_tetromino = tetris.add_tetromino_to_game_board_matrix(tetris.current_tetromino, 
                                                    tetris.game_board_matrix)
            tetris.tetris_window.redraw(matrix_and_tetromino,
                                    tetris.next_tetromino)
            time.sleep(0.5)


        binary_shape = np.where(np.array(tetris.current_tetromino.tetromino_shape)=='X', 1, 0)
        shape_in_box = np.sum(binary_shape, axis=0)

        for i in range(len(shape_in_box)):

            if shape_in_box[i]>0:
                column -= i
                break

        movement = column - posX

        if movement > 0:
            for _ in range(movement):

                tetris.move_right()

                matrix_and_tetromino = tetris.add_tetromino_to_game_board_matrix(tetris.current_tetromino, 
                                                    tetris.game_board_matrix)
                tetris.tetris_window.redraw(matrix_and_tetromino,
                                    tetris.next_tetromino)
                time.sleep(0.5)
        elif movement < 0:
            for _ in range(-movement):

                tetris.move_left()
                matrix_and_tetromino = tetris.add_tetromino_to_game_board_matrix(tetris.current_tetromino, 
                                                    tetris.game_board_matrix)
                tetris.tetris_window.redraw(matrix_and_tetromino,
                                    tetris.next_tetromino)
                time.sleep(0.5)

        time.sleep(0.3)
        tetris.hard_drop()        