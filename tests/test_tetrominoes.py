from src.tetrominoes import Tetrominoes
import random


def test_right_snake():
    """
    Test the initialization of the tetrominoes
    """
    random.seed(12)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == "right_snake"
    assert tetromino.tetromino_shape == (
        (None, "X", "X"),
        ("X", "X", None),
        (None, None, None),
    )
    assert tetromino.tetromino_color == "green"
    assert tetromino.tetromino_position == (0, 3)


def test_left_snake():
    """
    Test the initialization of the tetrominoes
    """
    random.seed(5)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == "left_snake"
    assert tetromino.tetromino_shape == (
        ("X", "X", None),
        (None, "X", "X"),
        (None, None, None),
    )
    assert tetromino.tetromino_color == "red"
    assert tetromino.tetromino_position == (0, 3)


def test_right_gun():
    """
    Test the initialization of the tetrominoes
    """
    random.seed(111)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == "right_gun"
    assert tetromino.tetromino_shape == (
        (None, None, "X"),
        ("X", "X", "X"),
        (None, None, None),
    )
    assert tetromino.tetromino_color == "orange"
    assert tetromino.tetromino_position == (0, 3)


def test_left_gun():
    """
    Test the initialization of the tetrominoes
    """
    random.seed(19)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == "left_gun"
    assert tetromino.tetromino_shape == (
        ("X", None, None),
        ("X", "X", "X"),
        (None, None, None),
    )
    assert tetromino.tetromino_color == "cyan"
    assert tetromino.tetromino_position == (0, 3)


def test_square():
    """
    Test the initialization of the tetrominoes
    """
    random.seed(1)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == "square"
    assert tetromino.tetromino_shape == (("X", "X"), ("X", "X"))
    assert tetromino.tetromino_color == "yellow"
    assert tetromino.tetromino_position == (0, 4)


def test_hat():
    """
    Test the initialization of the tetrominoes
    """
    random.seed(7)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == "hat"
    assert tetromino.tetromino_shape == (
        (None, "X", None),
        ("X", "X", "X"),
        (None, None, None),
    )
    assert tetromino.tetromino_color == "pink"
    assert tetromino.tetromino_position == (0, 3)


def test_long():
    """
    Test the initialization of the tetrominoes
    """
    random.seed(123)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == "long"
    assert tetromino.tetromino_shape == (
        (None, None, None, None),
        ("X", "X", "X", "X"),
        (None, None, None, None),
        (None, None, None, None),
    )
    assert tetromino.tetromino_color == "blue"
    assert tetromino.tetromino_position == (0, 3)


def test_rotate_hate():
    """
    Test rotate for hate tetromino
    """
    random.seed(7)
    tetromino = Tetrominoes()

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 1)
    assert new_shape == ((None, "X", None), (None, "X", "X"), (None, "X", None))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 2)
    assert new_shape == ((None, None, None), ("X", "X", "X"), (None, "X", None))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 3)
    assert new_shape == ((None, "X", None), ("X", "X", None), (None, "X", None))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 4)
    assert new_shape == ((None, "X", None), ("X", "X", "X"), (None, None, None))


def test_rotate_square():
    """
    Test rotate for square tetromino
    """
    random.seed(1)
    tetromino = Tetrominoes()

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 1)
    assert new_shape == (("X", "X"), ("X", "X"))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 2)
    assert new_shape == (("X", "X"), ("X", "X"))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 3)
    assert new_shape == (("X", "X"), ("X", "X"))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 4)
    assert new_shape == (("X", "X"), ("X", "X"))


def test_rotate_left_gun():
    """
    Test rotate for left gun tetromino
    """
    random.seed(19)
    tetromino = Tetrominoes()

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 1)
    assert new_shape == ((None, "X", "X"), (None, "X", None), (None, "X", None))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 2)
    assert new_shape == ((None, None, None), ("X", "X", "X"), (None, None, "X"))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 3)
    assert new_shape == ((None, "X", None), (None, "X", None), ("X", "X", None))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 4)
    assert new_shape == (("X", None, None), ("X", "X", "X"), (None, None, None))


def test_rotate_right_gun():
    """
    Test rotate for right gun tetromino
    """
    random.seed(111)
    tetromino = Tetrominoes()

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 1)
    assert new_shape == ((None, "X", None), (None, "X", None), (None, "X", "X"))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 2)
    assert new_shape == ((None, None, None), ("X", "X", "X"), ("X", None, None))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 3)
    assert new_shape == (("X", "X", None), (None, "X", None), (None, "X", None))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 4)
    assert new_shape == ((None, None, "X"), ("X", "X", "X"), (None, None, None))


def test_rotate_left_snake():
    """
    Test rotate for left snake tetromino
    """
    random.seed(5)
    tetromino = Tetrominoes()

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 1)
    assert new_shape == ((None, None, "X"), (None, "X", "X"), (None, "X", None))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 2)
    assert new_shape == ((None, None, None), ("X", "X", None), (None, "X", "X"))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 3)
    assert new_shape == ((None, "X", None), ("X", "X", None), ("X", None, None))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 4)
    assert new_shape == (("X", "X", None), (None, "X", "X"), (None, None, None))


def test_rotate_right_snake():
    """
    Test rotate for right snake tetromino
    """
    random.seed(12)
    tetromino = Tetrominoes()

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 1)
    assert new_shape == ((None, "X", None), (None, "X", "X"), (None, None, "X"))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 2)
    assert new_shape == ((None, None, None), (None, "X", "X"), ("X", "X", None))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 3)
    assert new_shape == (("X", None, None), ("X", "X", None), (None, "X", None))

    new_shape = tetromino.rotate(tetromino.tetromino_shape, 4)
    assert new_shape == ((None, "X", "X"), ("X", "X", None), (None, None, None))


def test_rotate_long():
    """
    Test rotate for long tetromino
    """
    random.seed(123)
    tetromino = Tetrominoes()
    new_shape = tetromino.rotate(tetromino.tetromino_shape, 1)
    assert new_shape == (
        (None, None, "X", None),
        (None, None, "X", None),
        (None, None, "X", None),
        (None, None, "X", None),
    )
    new_shape = tetromino.rotate(tetromino.tetromino_shape, 2)
    assert new_shape == (
        (None, None, None, None),
        (None, None, None, None),
        ("X", "X", "X", "X"),
        (None, None, None, None),
    )
    new_shape = tetromino.rotate(tetromino.tetromino_shape, 3)
    assert new_shape == (
        (None, "X", None, None),
        (None, "X", None, None),
        (None, "X", None, None),
        (None, "X", None, None),
    )
    new_shape = tetromino.rotate(tetromino.tetromino_shape, 4)
    assert new_shape == (
        (None, None, None, None),
        ("X", "X", "X", "X"),
        (None, None, None, None),
        (None, None, None, None),
    )


def test_move_down():
    """
    Test move down
    """
    random.seed(7)
    tetromino = Tetrominoes()

    tetromino.move_down()

    assert tetromino.tetromino_position == (1, 3)


def test_move_left():
    """
    Test move left
    """
    random.seed(7)
    tetromino = Tetrominoes()

    tetromino.move_left()

    assert tetromino.tetromino_position == (0, 2)


def test_move_right():
    """
    Test move right
    """
    random.seed(7)
    tetromino = Tetrominoes()

    tetromino.move_right()

    assert tetromino.tetromino_position == (0, 4)
