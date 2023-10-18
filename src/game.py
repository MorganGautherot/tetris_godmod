from src.windows import windows
from src.score import score
from src.tetrominoes import Tetrominoes
import src.config as config
import pygame
from src.bot import random_bot
import os

def get_sound(filename):
    return pygame.mixer.Sound(
        os.path.join(os.path.dirname(__file__), "resources", filename)
    )

class Tetris():

    def __init__(self):

        self.tetris_score = score()
        self.tetris_window = windows(self.tetris_score)
        self.matrix = dict()
        for y in range(config.MATRIX_HEIGHT):
            for x in range(config.MATRIX_WIDTH):
                self.matrix[(y, x)] = None
        self.current_tetromino = Tetrominoes()
        self.next_tetromino = Tetrominoes()

        self.clock = pygame.time.Clock()
        self.base_downwards_speed = 0.8  # Move down every 400 ms
        self.downwards_timer = 0

        self.linescleared_sound = get_sound("linecleared.wav")

    def tetromino_falls_over_time(self):
        timepassed = self.clock.tick(50)
        self.downwards_speed = self.base_downwards_speed ** (1 + self.tetris_score.level / 10.0)
        self.downwards_timer += timepassed/ 1000.0

        if self.downwards_timer > self.downwards_speed:
            self.move_down(self.current_tetromino, self.matrix)
            self.downwards_timer %= self.downwards_speed

    def add_tetromino_to_matrix(self, tetromino, matrix):
        """Add a tetromino to the matrix"""

        matrix_copy = matrix.copy()
        posY, posX = tetromino.tetromino_position
        shape = tetromino.tetromino_shape

        for x in range(posX, posX + len(shape)):
             for y in range(posY, posY + len(shape)):
                if shape[y - posY][x - posX]:
                    matrix_copy[(y, x)] = ('block', tetromino)

        return matrix_copy

    def fits_in_matrix(self, position, shape, matrix):
        """
        Checks if tetromino fits on the board
        """
        posY, posX = position
        for x in range(posX, posX + len(shape)):
            for y in range(posY, posY + len(shape)):

                if (
                    matrix.get((y, x), False) is False 
                    and shape[y - posY][x - posX] 
                    # outside matrix
                    or matrix.get((y, x)) 
                    and shape[y - posY][x - posX]
                    and matrix[(y, x)][0] != "shadow"
                    # coordinate is occupied by something else which isn't a shadow
                ):  
                    return False

        return True

    def user_action(self)->None:
        """Get user action and apply them to the game"""

        pressed = lambda key: event.type == pygame.KEYDOWN and event.key == key
        unpressed = lambda key: event.type == pygame.KEYUP and event.key == key

        events = pygame.event.get()
        
        for event in events:
            # Controls pausing and quitting the game.
            if event.type == pygame.QUIT:
                exit()
            elif pressed(pygame.K_ESCAPE):
                exit()

            # Controls movement of the tetromino
            elif pressed(pygame.K_LEFT) or pressed(pygame.K_a):
                self.downwards_timer = 0
                self.move_left(self.current_tetromino, self.matrix)
            elif pressed(pygame.K_RIGHT) or pressed(pygame.K_d):
                self.downwards_timer = 0
                self.move_right(self.current_tetromino, self.matrix)
            elif pressed(pygame.K_DOWN) or pressed(pygame.K_s):
                self.downwards_timer = 0
                self.move_down(self.current_tetromino, self.matrix)
            elif pressed(pygame.K_UP) or pressed(pygame.K_w):
                self.downwards_timer = 0
                self.rotation(self.current_tetromino, self.matrix)
            elif pressed(pygame.K_SPACE):
                self.hard_drop(self.current_tetromino, self.matrix)

    def rotation(self, tetromino, matrix)->None:
        """move the tetromino to the right"""
        new_shape = tetromino.rotate(tetromino.tetromino_shape, 1)
        posY, posX = tetromino.tetromino_position

        if self.fits_in_matrix((posY, posX), new_shape, matrix):
            tetromino.tetromino_shape = new_shape
        elif self.fits_in_matrix((posY, posX-1), new_shape, matrix):
            tetromino.tetromino_shape = new_shape
            tetromino.tetromino_position = (posY, posX-1)
        elif self.fits_in_matrix((posY, posX+1), new_shape, matrix):
            tetromino.tetromino_shape = new_shape
            tetromino.tetromino_position = (posY, posX+1)
        elif self.fits_in_matrix((posY, posX-2), new_shape, matrix):
            tetromino.tetromino_shape = new_shape
            tetromino.tetromino_position = (posY, posX-2)
        elif self.fits_in_matrix((posY, posX+2), new_shape, matrix):
            tetromino.tetromino_shape = new_shape
            tetromino.tetromino_position = (posY, posX+2)
        elif self.fits_in_matrix((posY, posX-3), new_shape, matrix):
            tetromino.tetromino_shape = new_shape
            tetromino.tetromino_position = (posY, posX-3)
        elif self.fits_in_matrix((posY, posX+3), new_shape, matrix):
            tetromino.tetromino_shape = new_shape
            tetromino.tetromino_position = (posY, posX+3)
        elif self.fits_in_matrix((posY, posX-4), new_shape, matrix):
            tetromino.tetromino_shape = new_shape
            tetromino.tetromino_position = (posY, posX-4)
        elif self.fits_in_matrix((posY, posX+4), new_shape, matrix):
            tetromino.tetromino_shape = new_shape
            tetromino.tetromino_position = (posY, posX+4)

    def move_right(self, tetromino, matrix)->None:
        """move the tetromino to the right"""
        posY, posX = tetromino.tetromino_position
        shape =  tetromino.tetromino_shape
        if self.fits_in_matrix((posY, posX+1), shape, matrix):
            tetromino.move_right()

    def move_left(self, tetromino, matrix)->None:
        """move the tetromino to the left"""
        posY, posX = tetromino.tetromino_position
        shape =  tetromino.tetromino_shape
        if self.fits_in_matrix((posY, posX-1), shape, matrix):
            tetromino.move_left()

    def move_down(self, tetromino, matrix)->None:
        """move the tetromino to the down"""
        posY, posX = tetromino.tetromino_position
        shape =  tetromino.tetromino_shape
        if self.fits_in_matrix((posY+1, posX), shape, matrix):
            tetromino.move_down()
        else : 
            self.fall_down()

    def fall_down(self):
        self.lock_tetromino()
        lines_cleared = self.remove_lines()

        if lines_cleared:
            self.tetris_score.mark_score(lines_cleared)

            if lines_cleared >= 4:
                self.linescleared_sound.play()

        else : 
            self.tetris_score.reset_combo()

    def last_valid_position(self, tetromino, matrix)-> None:
        posY, posX = tetromino.tetromino_position
        shape = tetromino.tetromino_shape
        new_posY = 1
        while self.fits_in_matrix((new_posY, posX), shape, matrix):
            new_posY += 1
        
        new_posY -= 1
        return (new_posY, posX), shape
    
    def hard_drop(self, tetromino, matrix):
        posY, posX = tetromino.tetromino_position
        (new_posY, posX), shape = self.last_valid_position(tetromino, matrix)
        tetromino.tetromino_position = (new_posY, posX)
        self.fall_down()


    def lock_tetromino(self)->None:
        """Lock the tetromino to the matrix"""

        self.matrix = self.add_tetromino_to_matrix(self.current_tetromino, 
                                                   self.matrix)
        

        self.set_tetrominoes()

    def set_tetrominoes(self)->None:
        """Get new tetrominoes"""

        self.current_tetromino = self.next_tetromino

        self.next_tetromino = Tetrominoes()

        # game over
        if not(self.fits_in_matrix(self.current_tetromino.tetromino_position, 
                            self.current_tetromino.tetromino_shape, 
                            self.matrix)):
            exit()

        
    def remove_lines(self):
        """
        Removes lines from the board
        """
        lines = []
        for y in range(config.MATRIX_HEIGHT):
            # Checks if row if full, for each row
            line = (y, [])
            for x in range(config.MATRIX_WIDTH):
                if self.matrix[(y, x)]:
                    line[1].append(x)
            if len(line[1]) == config.MATRIX_WIDTH:
                lines.append(y)

        for line in sorted(lines):
            # Moves lines down one row
            for x in range(config.MATRIX_WIDTH):
                self.matrix[(line, x)] = None
            for y in range(0, line + 1)[::-1]:
                for x in range(config.MATRIX_WIDTH):
                    self.matrix[(y, x)] = self.matrix.get((y - 1, x), None)

        return len(lines)
        