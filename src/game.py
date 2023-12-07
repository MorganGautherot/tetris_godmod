from src.windows import Windows
from src.score import Score
from src.tetrominoes import Tetrominoes
import src.config as config
from src.save_examples import dataframe_creation
import pygame
import pandas as pd


class Tetris:
    def __init__(self, take_picture: bool = False, display: bool = True) -> None:
        """
        Initialization of the game
        """

        # Save the frame of the game to train a deep learning modèle
        self.take_picture = take_picture

        self.display = display

        # Initialization of the scoring module
        self.tetris_score = Score()

        if self.display:  # pragma: no cover
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
            self.data_creation = dataframe_creation()

            # Dataframe initialization to save the tetromino's final position
            y_dataframe = pd.DataFrame(
                [], columns=("name", "path", "column", "rotation")
            )
            y_dataframe.to_csv("y_dataframe.csv", index=False)

            matrix_and_tetromino = self.add_tetromino_to_game_board_matrix(
                self.current_tetromino, self.game_board_matrix
            )

            self.data_creation.game_board_to_image(
                matrix_and_tetromino, self.current_tetromino
            )

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
                exit()
            elif pressed(pygame.K_ESCAPE):
                exit()

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

    def hard_drop(self) -> None:
        """
        Put the tetromino at the lowest possible position
        """
        _, posX = self.current_tetromino.tetromino_position
        (new_posY, posX) = self.last_valid_position(
            self.current_tetromino, self.game_board_matrix
        )
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

            self.tetris_window.redraw(matrix_and_tetromino, self.next_tetromino)

            self.data_creation.game_board_to_image(
                matrix_and_tetromino, self.current_tetromino
            )

        # game over
        if not (
            self.fits_in_game_board_matrix(
                self.current_tetromino.tetromino_position,
                self.current_tetromino.tetromino_shape,
                self.game_board_matrix,
            )
        ):  # pragma: no cover
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
