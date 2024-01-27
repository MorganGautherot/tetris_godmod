from src.windows import Windows
from src.score import Score
from src.tetrominoes import Tetrominoes
import src.config as config
from src.save_examples import dataframe_creation
import pygame
import pandas as pd
import numpy as np
import copy
import random
import os


class Tetris:
    def __init__(self, take_picture: bool = False, display: bool = True, training_id:int=0, seed:int=None) -> None:
        """
        Initialization of the game
        """

        random.seed(seed)     

        self.game_over = False

        # Save the frame of the game to train a deep learning modèle
        self.take_picture = take_picture

        self.display = display

        # Initialization of the scoring module
        self.tetris_score = Score()

        #if self.display:  
        if display: # pragma: no cover
            self.tetris_window = Windows(self.tetris_score)

        # Game board initialization
        self.game_board_matrix = dict()
        for y in range(config.MATRIX_HEIGHT):
            for x in range(config.MATRIX_WIDTH):
                self.game_board_matrix[(y, x)] = None

        # Initialisation of the current tetromino
        self.current_tetromino = Tetrominoes()

        # Initialisation of the nex tetromino
        self.next_tetromino = Tetrominoes()

        if self.take_picture:  # pragma: no cover
            # Initialization of the object to map game board into image
            self.data_creation = dataframe_creation(training_id)



            self.data_creation.game_board_to_image(self)


        # Initialization of the time game
        self.clock = pygame.time.Clock()
        # Move down every 400 ms
        self.base_downwards_speed = 0.8
        self.downwards_timer = 0

    def tetromino_falls_over_time(self) -> None:
        """
        After a preset time, the current tetromino moves down one square in the game board
        """

        timepassed = self.clock.tick(50)
        self.downwards_speed = self.base_downwards_speed ** (
            1 + self.tetris_score.level / 10.0
        )
        self.downwards_timer += timepassed / 1000.0

        # If the time exceeds the preset time, move the tetromino downwards
        if self.downwards_timer > self.downwards_speed:
            self.move_down()
            self.downwards_timer %= self.downwards_speed

    @staticmethod
    def add_tetromino_to_game_board_matrix(
        tetromino: Tetrominoes, game_board_matrix: dict
    ) -> dict:
        """
        Add a tetromino to the board game
        """

        game_board_matrix_copy = game_board_matrix.copy()
        posY, posX = tetromino.tetromino_position
        shape = tetromino.tetromino_shape

        for x in range(posX, posX + len(shape)):
            for y in range(posY, posY + len(shape)):
                if shape[y - posY][x - posX]:
                    game_board_matrix_copy[(y, x)] = tetromino.tetromino_color

        return game_board_matrix_copy

    @staticmethod
    def fits_in_game_board_matrix(
        position: tuple, shape: list, game_board_matrix: dict
    ) -> bool:
        """
        Checks if tetromino fits on the board
        """
        posY, posX = position
        for x in range(posX, posX + len(shape)):
            for y in range(posY, posY + len(shape)):
                if (  # outside board game
                    game_board_matrix.get((y, x), False) is False
                    and shape[y - posY][x - posX]
                    # coordinate is occupied by something else which isn't a shadow
                    or game_board_matrix.get((y, x))
                    and shape[y - posY][x - posX]
                ):
                    return False
        return True

    def user_action(self) -> None:  # pragma: no cover
        """
        Get user action and apply them to the game
        """

        pressed = lambda key: event.type == pygame.KEYDOWN and event.key == key

        events = pygame.event.get()

        for event in events:
            # Controls pausing and quitting the game.
            if event.type == pygame.QUIT:
                self.game_over = True
            elif pressed(pygame.K_ESCAPE):
                self.game_over = True

            # Controls movement of the tetromino
            elif pressed(pygame.K_LEFT) or pressed(pygame.K_a):
                self.downwards_timer = 0
                self.move_left()
            elif pressed(pygame.K_RIGHT) or pressed(pygame.K_d):
                self.downwards_timer = 0
                self.move_right()
            elif pressed(pygame.K_DOWN) or pressed(pygame.K_s):
                self.downwards_timer = 0
                self.move_down()
            elif pressed(pygame.K_UP) or pressed(pygame.K_w):
                self.downwards_timer = 0
                self.rotation()
            elif pressed(pygame.K_SPACE):
                self.hard_drop()

    def rotation(self) -> None:
        """
        Rotate the tetromino
        """

        new_shape = self.current_tetromino.rotate(
            self.current_tetromino.tetromino_shape, times=1
        )
        posY, posX = self.current_tetromino.tetromino_position

        if self.fits_in_game_board_matrix(
            (posY, posX), new_shape, self.game_board_matrix
        ):
            self.current_tetromino.tetromino_shape = new_shape
        elif self.fits_in_game_board_matrix(
            (posY, posX - 1), new_shape, self.game_board_matrix
        ):
            self.current_tetromino.tetromino_shape = new_shape
            self.current_tetromino.tetromino_position = (posY, posX - 1)
        elif self.fits_in_game_board_matrix(
            (posY, posX + 1), new_shape, self.game_board_matrix
        ):
            self.current_tetromino.tetromino_shape = new_shape
            self.current_tetromino.tetromino_position = (posY, posX + 1)
        elif self.fits_in_game_board_matrix(
            (posY - 1, posX), new_shape, self.game_board_matrix
        ):
            self.current_tetromino.tetromino_shape = new_shape
            self.current_tetromino.tetromino_position = (posY - 1, posX)
        elif self.fits_in_game_board_matrix(
            (posY - 1, posX + 1), new_shape, self.game_board_matrix
        ):
            self.current_tetromino.tetromino_shape = new_shape
            self.current_tetromino.tetromino_position = (posY - 1, posX + 1)
        elif self.fits_in_game_board_matrix(
            (posY - 1, posX - 1), new_shape, self.game_board_matrix
        ):
            self.current_tetromino.tetromino_shape = new_shape
            self.current_tetromino.tetromino_position = (posY - 1, posX - 1)
        elif self.fits_in_game_board_matrix(
            (posY - 2, posX), new_shape, self.game_board_matrix
        ):
            self.current_tetromino.tetromino_shape = new_shape
            self.current_tetromino.tetromino_position = (posY - 2, posX)
        elif self.fits_in_game_board_matrix(
            (posY, posX - 2), new_shape, self.game_board_matrix
        ):
            self.current_tetromino.tetromino_shape = new_shape
            self.current_tetromino.tetromino_position = (posY, posX - 2)
        elif self.fits_in_game_board_matrix(
            (posY, posX + 2), new_shape, self.game_board_matrix
        ):
            self.current_tetromino.tetromino_shape = new_shape
            self.current_tetromino.tetromino_position = (posY, posX + 2)

    def move_right(self) -> None:
        """
        Move the tetromino to the right
        """
        posY, posX = self.current_tetromino.tetromino_position
        shape = self.current_tetromino.tetromino_shape
        if self.fits_in_game_board_matrix(
            (posY, posX + 1), shape, self.game_board_matrix
        ):
            self.current_tetromino.move_right()

    def move_left(self) -> None:
        """
        Move the tetromino to the left
        """
        posY, posX = self.current_tetromino.tetromino_position
        shape = self.current_tetromino.tetromino_shape
        if self.fits_in_game_board_matrix(
            (posY, posX - 1), shape, self.game_board_matrix
        ):
            self.current_tetromino.move_left()

    def move_down(self) -> None:
        """
        Move the tetromino to the down
        """
        posY, posX = self.current_tetromino.tetromino_position
        shape = self.current_tetromino.tetromino_shape
        if self.fits_in_game_board_matrix(
            (posY + 1, posX), shape, self.game_board_matrix
        ):
            self.current_tetromino.move_down()
        else:
            self.fall_down()

    def fall_down(self) -> None:
        """
        The tetromino has arrived at the bottom of the platform
        """
        # Add the tetromino to the board
        self.lock_tetromino()

        # Remove complete lines
        lines_cleared = self.remove_lines()

        # Update the score
        if lines_cleared:
            self.tetris_score.mark_score(lines_cleared)
        else:
            self.tetris_score.reset_combo()

    def last_valid_position(
        self, tetromino: Tetrominoes, game_board_matrix: dict
    ) -> tuple:
        """
        Return the last valid position for the lowest lines at the current column position
        """
        _, posX = tetromino.tetromino_position
        shape = tetromino.tetromino_shape
        new_posY = 1
        while self.fits_in_game_board_matrix(
            (new_posY, posX), shape, game_board_matrix
        ):
            new_posY += 1

        new_posY -= 1
        return (new_posY, posX)

    def is_hidden_position(
        self, tetromino: Tetrominoes, game_board_matrix: dict
    ) -> bool:
        """
        Return if there is a hidden position at the current column position
        """
        hidden = False
        posY, posX = self.last_valid_position(tetromino, game_board_matrix)
        shape = tetromino.tetromino_shape
        new_posY = posY + 1
        while new_posY <= 20: 
            if self.fits_in_game_board_matrix(
            (new_posY, posX), shape, game_board_matrix
        ):
                hidden = True

            elif not(self.fits_in_game_board_matrix(
            (new_posY, posX), shape, game_board_matrix
        )) and hidden:
                
                new_posY -= 1
                break
            new_posY += 1

        return hidden, new_posY, posX
    
    def is_valid_hidden_position(self, 
                                 tetromino: Tetrominoes, 
                                 game_board_matrix:dict, 
                                 valid_matrix:np.ndarray)->bool:
        
        """
        Check if the hidden positon is valid
        """
        
        posY, posX = tetromino.tetromino_position
        shape = tetromino.tetromino_shape

        position_seen = [(posY, posX)]
        position_to_see = [(posY, posX-1), (posY, posX+1), (posY-1, posX)]

        valid_hidden_position = False
        number_of_valid_pixel = np.sum(valid_matrix)

        while len(position_to_see) > 0:

            next_posY, newt_posX = position_to_see[0]
            position_seen.append(position_to_see[0])
            position_to_see.remove(position_to_see[0])

            if self.fits_in_game_board_matrix(
                (next_posY, newt_posX), shape, game_board_matrix):

                if  not((next_posY, newt_posX-1) in position_seen):
                    position_to_see.append((next_posY, newt_posX-1))
                if  not((next_posY, newt_posX+1) in position_seen):
                    position_to_see.append((next_posY, newt_posX+1))
                if  not((next_posY-1, newt_posX) in position_seen):
                    position_to_see.append((next_posY-1, newt_posX))
                if  not((next_posY+1, newt_posX) in position_seen):
                    position_to_see.append((next_posY+1, newt_posX))
        

                valid_matrix_copy = copy.deepcopy(valid_matrix)
                    
                for x in range(newt_posX, newt_posX + len(shape)):
                    for y in range(next_posY, next_posY + len(shape)):
                        if shape[y - next_posY][x - newt_posX]:
                            valid_matrix_copy[(y, x)] = 1
                
                if number_of_valid_pixel == np.sum(valid_matrix_copy):
                    valid_hidden_position = True
                    break
                
        return valid_hidden_position
    
    def hidden_position(self, tetromino:Tetrominoes, game_board_matrix:dict)->tuple:
        '''
        Return the valid hidden position if there is one
        '''

        valid_matrix = self.valid_area(game_board_matrix)

        is_hidden, new_posY, posX = self.is_hidden_position(tetromino, game_board_matrix)

        if is_hidden :

            current_tetromino_copy = copy.deepcopy(tetromino)
            current_tetromino_copy.tetromino_position = (new_posY, posX)

            is_valid_hidden = self.is_valid_hidden_position(current_tetromino_copy,
                                                            game_board_matrix,
                                                            valid_matrix)


            if is_valid_hidden:
                return is_valid_hidden, new_posY, posX
        return False, new_posY, posX

     
    
    
    def valid_area(
        self, game_board_matrix: dict
    ) -> bool:
        """
        Determine the valid area in the game_board_matrix
        """
        valid_matrix = np.zeros((config.MATRIX_HEIGHT, config.MATRIX_WIDTH))
        for column in range(0, config.MATRIX_WIDTH):
            not_tetromino_yet = True
            for line in range(0, config.MATRIX_HEIGHT):
                if not(game_board_matrix[line, column]) and not_tetromino_yet:
                    valid_matrix[line, column] = 1
                elif game_board_matrix[line, column]:
                    not_tetromino_yet = False
                    
        return valid_matrix


    def hard_drop(self) -> None:
        """
        Put the tetromino at the lowest possible position
        """
        posY, posX = self.current_tetromino.tetromino_position
        (new_posY, posX) = self.last_valid_position(
            self.current_tetromino, self.game_board_matrix
        )
        self.tetris_score.score += 10* (new_posY-posY)
        self.current_tetromino.tetromino_position = (new_posY, posX)
        self.fall_down()

    def lock_tetromino(self) -> None:
        """
        Lock the tetromino to the matrix
        """

        if self.take_picture:  # pragma: no cover
            matrix_and_tetromino = self.add_tetromino_to_game_board_matrix(
                self.current_tetromino, self.game_board_matrix
            )

            if self.display :
                self.tetris_window.redraw(matrix_and_tetromino, self.next_tetromino)

            self.data_creation.add_row_dataframe_y(self.current_tetromino)

        self.game_board_matrix = self.add_tetromino_to_game_board_matrix(
            self.current_tetromino, self.game_board_matrix
        )

        self.set_tetrominoes()

    def set_tetrominoes(self) -> None:
        """
        Get new tetrominoes
        """

        self.current_tetromino = self.next_tetromino

        self.next_tetromino = Tetrominoes()

        if self.take_picture:  # pragma: no cover
            matrix_and_tetromino = self.add_tetromino_to_game_board_matrix(
                self.current_tetromino, self.game_board_matrix
            )
            if self.display:
                self.tetris_window.redraw(matrix_and_tetromino, self.next_tetromino)

            self.data_creation.game_board_to_image(self)

        # game over
        if not (
            self.fits_in_game_board_matrix(
                self.current_tetromino.tetromino_position,
                self.current_tetromino.tetromino_shape,
                self.game_board_matrix,
            )
        ):  # pragma: no cover
            self.game_over = True

    def remove_lines(self):
        """
        Removes lines from the board
        """
        lines = []
        for y in range(config.MATRIX_HEIGHT):
            # Checks if row if full, for each row
            line = (y, [])
            for x in range(config.MATRIX_WIDTH):
                if self.game_board_matrix[(y, x)]:
                    line[1].append(x)
            if len(line[1]) == config.MATRIX_WIDTH:
                lines.append(y)

        for line in sorted(lines):
            # Moves lines down one row
            for x in range(config.MATRIX_WIDTH):
                self.game_board_matrix[(line, x)] = None
            for y in range(0, line + 1)[::-1]:
                for x in range(config.MATRIX_WIDTH):
                    self.game_board_matrix[(y, x)] = self.game_board_matrix.get(
                        (y - 1, x), None
                    )

        return len(lines)
