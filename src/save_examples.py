import numpy as np
import cv2
import src.config as config
from src.tetrominoes import Tetrominoes
import pandas as pd
import os

class dataframe_creation():

    def __init__(self, training_id:int=0):
        self.number_screenshot = 0
        self.training_id = training_id

        # Dataframe initialization to save the tetromino's final position
        y_dataframe = pd.DataFrame(
            [], columns=("name", "path", "column", "rotation")
        )
        y_dataframe.to_csv(f'y_{self.training_id}_dataframe.csv', index=False)

    def integrate_tetromino_in_board(self, 
                                     tetromino, 
                                     game_board_matrix,
                                     is_current=True):

        match tetromino.tetromino_name:
            case 'long':
                if is_current:
                    game_board_matrix[0, 0] = 255
                    game_board_matrix[0, 1] = 255
                    game_board_matrix[0, 2] = 255
                    game_board_matrix[0, 3] = 255
                else:
                    game_board_matrix[0, -1] = 255
                    game_board_matrix[0, -2] = 255
                    game_board_matrix[0, -3] = 255
                    game_board_matrix[0, -4] = 255                   
            case 'right_gun':
                if is_current:
                    game_board_matrix[4, 0] = 255
                    game_board_matrix[4, 1] = 255
                    game_board_matrix[4, 2] = 255
                    game_board_matrix[3, 2] = 255
                else:
                    game_board_matrix[4, -1] = 255
                    game_board_matrix[4, -2] = 255
                    game_board_matrix[4, -3] = 255
                    game_board_matrix[3, -1] = 255                    
            case 'square':
                if is_current:
                    game_board_matrix[6, 0] = 255
                    game_board_matrix[6, 1] = 255
                    game_board_matrix[7, 0] = 255
                    game_board_matrix[7, 1] = 255
                else:
                    game_board_matrix[6, -1] = 255
                    game_board_matrix[6, -2] = 255
                    game_board_matrix[7, -1] = 255
                    game_board_matrix[7, -2] = 255
            case 'left_gun':
                if is_current:
                    game_board_matrix[10, 0] = 255
                    game_board_matrix[10, 1] = 255
                    game_board_matrix[10, 2] = 255
                    game_board_matrix[9, 0] = 255
                else:
                    game_board_matrix[10, -1] = 255
                    game_board_matrix[10, -2] = 255
                    game_board_matrix[10, -3] = 255
                    game_board_matrix[9, -3] = 255
            case 'left_snake':
                if is_current:
                    game_board_matrix[12, 0] = 255
                    game_board_matrix[12, 1] = 255
                    game_board_matrix[13, 1] = 255
                    game_board_matrix[13, 2] = 255   
                else:
                    game_board_matrix[12, -3] = 255
                    game_board_matrix[12, -2] = 255
                    game_board_matrix[13, -2] = 255
                    game_board_matrix[13, -1] = 255
            case 'hat':
                if is_current:
                    game_board_matrix[15, 0] = 255
                    game_board_matrix[15, 1] = 255
                    game_board_matrix[15, 2] = 255
                    game_board_matrix[14, 1] = 255   
                else:
                    game_board_matrix[15, -1] = 255
                    game_board_matrix[15, -2] = 255
                    game_board_matrix[15, -3] = 255
                    game_board_matrix[14, -2] = 255  
            case 'right_snake':
                if is_current:
                    game_board_matrix[19, 0] = 255
                    game_board_matrix[19, 1] = 255
                    game_board_matrix[18, 1] = 255
                    game_board_matrix[18, 2] = 255
                else :
                    game_board_matrix[18, -1] = 255
                    game_board_matrix[18, -2] = 255
                    game_board_matrix[19, -2] = 255
                    game_board_matrix[19, -3] = 255
        return game_board_matrix

    def game_board_to_image(self, 
                            tetris
                            )->None:
        """
        Transform the game board matrix into an image
        """

        saving_path = f'X_{self.training_id}/'

        if not(os.path.exists(saving_path)):
            
            os.mkdir(saving_path)
            

        image_matrix = np.zeros((config.MATRIX_HEIGHT, config.MATRIX_WIDTH+12))

        for key, values in tetris.game_board_matrix.items():
            y, x = key
            if not(values is None):
                image_matrix[y, x+6] = 255

        image_matrix = self.integrate_tetromino_in_board(tetris.current_tetromino,
                                                         image_matrix,
                                                         True) 

        image_matrix = self.integrate_tetromino_in_board(tetris.next_tetromino,
                                                         image_matrix,
                                                         False) 

        self.tetromino_name = tetris.current_tetromino.tetromino_name.replace('_', '-') 
        self.path = f'{saving_path}/{self.number_screenshot}_{self.tetromino_name}.png'

        cv2.imwrite(self.path, image_matrix[:, :])

        self.number_screenshot += 1

    def add_row_dataframe_y(self, 
                            current_tetromino:Tetrominoes
                            )->None:

        dataframe_path = f'y_{self.training_id}_dataframe.csv'

        y_dataframe = pd.read_csv(dataframe_path)

        first_column = self.shape_into_first_column(current_tetromino)

        new_row = pd.DataFrame([[self.tetromino_name,
                                 self.path,
                                 first_column,
                                 current_tetromino.rotation]], columns=('name', 'path', 'column', 'rotation'))
        new_y_dataframe = pd.concat([y_dataframe, new_row]).reset_index(drop=True)

        print(f'rotation : {current_tetromino.rotation}')
        print(f'column : {first_column}')
        new_y_dataframe.to_csv(dataframe_path, index=False)

    def shape_into_first_column(self, tetromino:Tetrominoes)->np.ndarray:
        """
        Return the first column where the shape is 
        """

        column = tetromino.tetromino_position[1]
        print(f"original column : {column}")


        binary_shape = np.where(np.array(tetromino.tetromino_shape)=='X', 1, 0)

        shape_in_box = np.sum(binary_shape, axis=0)


        for i in range(len(shape_in_box)):

            if shape_in_box[i]>0:
                column += i
                break
        return column