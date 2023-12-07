import numpy as np
import cv2
import src.config as config
from src.tetrominoes import Tetrominoes
import pandas as pd
import os

class dataframe_creation():

    def __init__(self):
        self.number_screenshot = 0

    def game_board_to_image(self, 
                            matrix_and_tetromino:dict, 
                            current_tetromino:Tetrominoes
                            )->None:
        """
        Transform the game board matrix into an image
        """

        if not(os.path.exists('X/')):
            os.system('mkdir X')

        image_matrix = np.zeros((config.MATRIX_HEIGHT, config.MATRIX_WIDTH))

        for key, values in matrix_and_tetromino.items():

            if not(values is None):
                image_matrix[key] = 255

        self.tetromino_name = current_tetromino.tetromino_name.replace('_', '-') 
        self.path = f'X/{self.number_screenshot}_{self.tetromino_name}.png'
        cv2.imwrite(self.path, image_matrix[:, :])

        self.number_screenshot += 1

    def add_row_dataframe_y(self, 
                            current_tetromino:Tetrominoes
                            )->None:

        y_dataframe = pd.read_csv('y_dataframe.csv')

        first_column = self.shape_into_first_column(current_tetromino)

        new_row = pd.DataFrame([[self.tetromino_name,
                                 self.path,
                                 first_column,
                                 current_tetromino.rotation]], columns=('name', 'path', 'column', 'rotation'))
        new_y_dataframe = pd.concat([y_dataframe, new_row]).reset_index(drop=True)

        print(f'rotation : {current_tetromino.rotation}')
        print(f'column : {first_column}')
        new_y_dataframe.to_csv('y_dataframe.csv', index=False)

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