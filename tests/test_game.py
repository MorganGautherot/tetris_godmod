from src.game import Tetris
import src.config as config
import time, random
from src.tetrominoes import Tetrominoes
import numpy as np


def test_initialization_game_board_matrix():
    """
    Test the initialization of the game board matrix
    """

    tetris_game = Tetris(display=False)

    for y in range(config.MATRIX_HEIGHT):
        for x in range(config.MATRIX_WIDTH):
            assert tetris_game.game_board_matrix[(y, x)] == None


def test_not_falling_tetromino_falls_over_time():
    """
    Test the falling of the tetromino
    """
    random.seed(12)
    tetris_game = Tetris(display=False)
    old_position = tetris_game.current_tetromino.tetromino_position
    time.sleep(0.1)
    tetris_game.tetromino_falls_over_time()

    assert tetris_game.current_tetromino.tetromino_position[0] == 0


def test_falling_tetromino_falls_over_time():
    """
    Test the falling of the tetromino
    """
    random.seed(12)
    tetris_game = Tetris(display=False)
    time.sleep(1)
    tetris_game.tetromino_falls_over_time()

    assert tetris_game.current_tetromino.tetromino_position[0] == 1


def test_add_tetromino_to_game_board_matrix():
    """
    Test the append of tetromino to the game board matrix
    """

    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (18, 2),
        (18, 3),
        (18, 4),
        (19, 4),
        (19, 5),
        (18, 8),
        (18, 9),
        (19, 8),
        (19, 9),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
    ]

    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "pink"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "red"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "yellow"

    random.seed(12)
    tetromino = Tetrominoes()

    new_game_board_matrix = Tetris.add_tetromino_to_game_board_matrix(
        tetromino, tetris_game.game_board_matrix
    )

    for id_line in np.arange(config.MATRIX_HEIGHT):
        for id_column in np.arange(config.MATRIX_WIDTH):
            if (id_line, id_column) in list_of_coordonates:
                assert not (new_game_board_matrix[(id_line, id_column)] is None)
            else:
                assert new_game_board_matrix[(id_line, id_column)] is None


def test_fits_in_game_board_matrix_false():
    """
    Test when a tetromino do not fit in the board game matrix
    """

    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (18, 2),
        (18, 3),
        (18, 4),
        (19, 4),
        (19, 5),
        (18, 8),
        (18, 9),
        (19, 8),
        (19, 9),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
    ]

    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "pink"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "red"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "yellow"

    random.seed(12)
    tetromino = Tetrominoes()

    new_tetromino_position = (19, 0)
    tetromino_shape = tetromino.tetromino_shape

    assert (
        Tetris.fits_in_game_board_matrix(
            new_tetromino_position, tetromino_shape, tetris_game.game_board_matrix
        )
        == False
    )


def test_fits_in_game_board_matrix_True():
    """
    Test when a tetromino fit in the board game matrix
    """

    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (18, 2),
        (18, 3),
        (18, 4),
        (19, 4),
        (19, 5),
        (18, 8),
        (18, 9),
        (19, 8),
        (19, 9),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
    ]

    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "pink"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "red"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "yellow"

    random.seed(12)
    tetromino = Tetrominoes()

    new_tetromino_position = (0, 5)
    tetromino_shape = tetromino.tetromino_shape

    assert (
        Tetris.fits_in_game_board_matrix(
            new_tetromino_position, tetromino_shape, tetris_game.game_board_matrix
        )
        == True
    )


def test_rotation_without_move():
    """
    Test when a rotation is possible without moving
    """
    random.seed(12)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (18, 2),
        (18, 3),
        (18, 4),
        (19, 4),
        (19, 5),
        (18, 8),
        (18, 9),
        (19, 8),
        (19, 9),
        (0, 4),
        (0, 5),
        (1, 3),
        (1, 4),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "pink"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "pink"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "red"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "red"

    tetris_game.game_board_matrix[list_of_coordonates[12]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "yellow"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "yellow"

    tetris_game.current_tetromino.tetromino_position = (10, 4)

    tetris_game.rotation()

    assert tetris_game.current_tetromino.tetromino_position == (10, 4)


def test_rotation_with_one_move_left():
    """
    Test when a rotation is possible with one move left
    """
    random.seed(111)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 6),
        (17, 6),
        (18, 6),
        (19, 6),
        (15, 6),
        (14, 6),
        (13, 6),
        (12, 6),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (15, 4)
    tetris_game.current_tetromino.tetromino_shape = (
        tetris_game.current_tetromino.rotate(
            tetris_game.current_tetromino.tetromino_shape, 3
        )
    )

    tetris_game.rotation()

    assert tetris_game.current_tetromino.tetromino_position == (15, 3)


def test_rotation_with_one_move_right():
    """
    Test when a rotation is possible with one move right
    """
    random.seed(111)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 4),
        (17, 4),
        (18, 4),
        (19, 4),
        (15, 4),
        (14, 4),
        (13, 4),
        (12, 4),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (15, 4)
    tetris_game.current_tetromino.tetromino_shape = (
        tetris_game.current_tetromino.rotate(
            tetris_game.current_tetromino.tetromino_shape, 1
        )
    )

    tetris_game.rotation()

    assert tetris_game.current_tetromino.tetromino_position == (15, 5)


def test_rotation_with_two_move_right():
    """
    Test when a rotation is possible with two move right
    """
    random.seed(123)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 4),
        (17, 4),
        (18, 4),
        (19, 4),
        (15, 4),
        (14, 4),
        (13, 4),
        (12, 4),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (15, 3)
    tetris_game.current_tetromino.tetromino_shape = (
        tetris_game.current_tetromino.rotate(
            tetris_game.current_tetromino.tetromino_shape, 1
        )
    )

    tetris_game.rotation()

    assert tetris_game.current_tetromino.tetromino_position == (15, 5)


def test_rotation_with_two_move_left():
    """
    Test when a rotation is possible with two move left
    """
    random.seed(123)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 6),
        (17, 6),
        (18, 6),
        (19, 6),
        (15, 6),
        (14, 6),
        (13, 6),
        (12, 6),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (15, 4)
    tetris_game.current_tetromino.tetromino_shape = (
        tetris_game.current_tetromino.rotate(
            tetris_game.current_tetromino.tetromino_shape, 3
        )
    )

    tetris_game.rotation()

    assert tetris_game.current_tetromino.tetromino_position == (15, 2)


def test_rotation_with_one_move_up():
    """
    Test when a rotation is possible with one move left
    """
    random.seed(123)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 6),
        (17, 6),
        (18, 6),
        (19, 6),
        (16, 3),
        (17, 3),
        (18, 3),
        (19, 3),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (15, 4)
    tetris_game.current_tetromino.tetromino_shape = (
        tetris_game.current_tetromino.rotate(
            tetris_game.current_tetromino.tetromino_shape, 3
        )
    )

    tetris_game.rotation()

    assert tetris_game.current_tetromino.tetromino_position == (14, 4)


def test_rotation_with_one_move_up_one_move_right():
    """
    Test when a rotation is possible with one move up one move right
    """
    random.seed(12)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 6),
        (17, 6),
        (18, 6),
        (19, 6),
        (15, 6),
        (14, 6),
        (13, 6),
        (12, 6),
        (16, 3),
        (17, 3),
        (18, 3),
        (19, 3),
        (15, 3),
        (14, 3),
        (13, 3),
        (12, 3),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (11, 3)
    tetris_game.current_tetromino.tetromino_shape = (
        tetris_game.current_tetromino.rotate(
            tetris_game.current_tetromino.tetromino_shape, 1
        )
    )

    tetris_game.rotation()

    assert tetris_game.current_tetromino.tetromino_position == (10, 4)


def test_rotation_with_two_move_up():
    """
    Test when a rotation is possible with two move up
    """
    random.seed(12)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 6),
        (17, 6),
        (18, 6),
        (19, 6),
        (15, 6),
        (14, 6),
        (13, 6),
        (12, 6),
        (11, 6),
        (16, 3),
        (17, 3),
        (18, 3),
        (19, 3),
        (15, 3),
        (14, 3),
        (13, 3),
        (12, 3),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[16]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (11, 3)
    tetris_game.current_tetromino.tetromino_shape = (
        tetris_game.current_tetromino.rotate(
            tetris_game.current_tetromino.tetromino_shape, 1
        )
    )

    tetris_game.rotation()

    assert tetris_game.current_tetromino.tetromino_position == (9, 3)


def test_rotation_with_one_move_up_one_move_left():
    """
    Test when a rotation is possible with one move up one move left
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 6),
        (17, 6),
        (18, 6),
        (19, 6),
        (15, 6),
        (14, 6),
        (13, 6),
        (12, 6),
        (16, 3),
        (17, 3),
        (18, 3),
        (19, 3),
        (15, 3),
        (14, 3),
        (13, 3),
        (12, 3),
        (12, 5),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[12]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[13]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[14]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[15]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[16]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (11, 3)
    tetris_game.current_tetromino.tetromino_shape = (
        tetris_game.current_tetromino.rotate(
            tetris_game.current_tetromino.tetromino_shape, 1
        )
    )

    tetris_game.rotation()

    assert tetris_game.current_tetromino.tetromino_position == (10, 2)


def test_move_left_not_possible():
    """
    Test when a move left is not possible
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 4),
        (17, 4),
        (18, 4),
        (19, 4),
        (15, 4),
        (14, 4),
        (13, 4),
        (12, 4),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (12, 5)

    tetris_game.move_left()

    assert tetris_game.current_tetromino.tetromino_position == (12, 5)


def test_move_left_possible():
    """
    Test when a move left is not possible
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 4),
        (17, 4),
        (18, 4),
        (19, 4),
        (15, 4),
        (14, 4),
        (13, 4),
        (12, 4),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (12, 6)

    tetris_game.move_left()

    assert tetris_game.current_tetromino.tetromino_position == (12, 5)


def test_move_right_not_possible():
    """
    Test when a move right is possible
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 6),
        (17, 6),
        (18, 6),
        (19, 6),
        (15, 6),
        (14, 6),
        (13, 6),
        (12, 6),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (12, 2)

    tetris_game.move_right()

    assert tetris_game.current_tetromino.tetromino_position == (12, 3)


def test_move_right_possible():
    """
    Test when a move right is possible
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (16, 6),
        (17, 6),
        (18, 6),
        (19, 6),
        (15, 6),
        (14, 6),
        (13, 6),
        (12, 6),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (12, 3)

    tetris_game.move_right()

    assert tetris_game.current_tetromino.tetromino_position == (12, 3)


def test_move_down_possible():
    """
    Test when a move down is possible
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [(16, 4), (17, 4), (18, 4), (19, 4)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (12, 4)

    tetris_game.move_down()

    assert tetris_game.current_tetromino.tetromino_position == (13, 4)


def test_move_down_not_possible():
    """
    Test when a move down is possible
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [(16, 4), (17, 4), (18, 4), (19, 4)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (14, 4)

    tetris_game.move_down()

    assert tetris_game.current_tetromino.tetromino_position == (0, 3)


def test_fall_down_no_lines_cleared():
    """
    Test when a fall down without line clear
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [(16, 4), (17, 4), (18, 4), (19, 4)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (14, 4)

    tetris_game.fall_down()

    assert tetris_game.current_tetromino.tetromino_position == (0, 3)
    assert tetris_game.current_tetromino.tetromino_name == "long"
    assert tetris_game.tetris_score.combo == 1


def test_fall_down_lines_cleared():
    """
    Test when a fall down with line clear
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (19, 4),
        (19, 5),
        (19, 6),
        (19, 7),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.rotation()
    tetris_game.rotation()
    tetris_game.rotation()
    tetris_game.current_tetromino.tetromino_position = (17, 8)

    tetris_game.fall_down()

    for col in np.arange(9):
        assert tetris_game.game_board_matrix[(19, col)] == None
    assert tetris_game.tetris_score.combo == 2
    assert tetris_game.current_tetromino.tetromino_position == (0, 3)
    assert tetris_game.current_tetromino.tetromino_name == "long"


def test_last_valid_position():
    """
    Test last valid position for a tetromino
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [(19, 0), (19, 1), (19, 2), (19, 3)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (0, 0)

    new_posY, posX = tetris_game.last_valid_position(
        tetris_game.current_tetromino, tetris_game.game_board_matrix
    )

    assert (new_posY, posX) == (17, 0)


def test_hard_drop():
    """
    Test hard_drop
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [(19, 0), (19, 1), (19, 2), (19, 3)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (0, 3)

    tetris_game.hard_drop()

    assert tetris_game.current_tetromino.tetromino_position == (0, 3)
    assert tetris_game.current_tetromino.tetromino_name == "long"
    assert tetris_game.game_board_matrix[(18, 3)] == "cyan"
    assert tetris_game.game_board_matrix[(18, 4)] == "cyan"
    assert tetris_game.game_board_matrix[(18, 5)] == "cyan"
    assert tetris_game.game_board_matrix[(17, 3)] == "cyan"


def test_lock_tetromino():
    """
    Test the function to lock a tetromino to the board
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [(19, 0), (19, 1), (19, 2), (19, 3)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (10, 3)

    tetris_game.lock_tetromino()

    assert tetris_game.current_tetromino.tetromino_position == (0, 3)
    assert tetris_game.current_tetromino.tetromino_name == "long"
    assert tetris_game.game_board_matrix[(11, 3)] == "cyan"
    assert tetris_game.game_board_matrix[(11, 4)] == "cyan"
    assert tetris_game.game_board_matrix[(11, 5)] == "cyan"
    assert tetris_game.game_board_matrix[(10, 3)] == "cyan"


def test_set_tetrominoes():
    """
    Test set a new tetromino
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [(19, 0), (19, 1), (19, 2), (19, 3)]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.current_tetromino.tetromino_position = (10, 3)

    tetris_game.set_tetrominoes()

    assert tetris_game.current_tetromino.tetromino_position == (0, 3)
    assert tetris_game.current_tetromino.tetromino_name == "long"


def test_remove_lines():
    """
    Test remove lines
    """
    random.seed(19)
    tetris_game = Tetris(display=False)

    list_of_coordonates = [
        (19, 0),
        (19, 1),
        (19, 2),
        (19, 3),
        (19, 4),
        (19, 5),
        (19, 6),
        (19, 7),
        (19, 8),
        (19, 9),
        (18, 9),
        (18, 8),
    ]
    tetris_game.game_board_matrix[list_of_coordonates[0]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[1]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[2]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[3]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[4]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[5]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[6]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[7]] = "blue"

    tetris_game.game_board_matrix[list_of_coordonates[8]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[9]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[10]] = "blue"
    tetris_game.game_board_matrix[list_of_coordonates[11]] = "blue"

    number_lines_cleared = tetris_game.remove_lines()

    assert number_lines_cleared == 1
    assert tetris_game.game_board_matrix[(19, 0)] is None
    assert tetris_game.game_board_matrix[(19, 1)] is None
    assert tetris_game.game_board_matrix[(19, 2)] is None
    assert tetris_game.game_board_matrix[(19, 3)] is None
    assert tetris_game.game_board_matrix[(19, 4)] is None
    assert tetris_game.game_board_matrix[(19, 5)] is None
    assert tetris_game.game_board_matrix[(19, 6)] is None
    assert tetris_game.game_board_matrix[(19, 7)] is None
