from src.tetrominoes import Tetrominoes
import random

def test_right_snake():
    """ Test the initialization of the tetrominoes"""
    random.seed(12)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == 'right_snake'
    assert tetromino.tetromino_shape == ((None,"X","X"),
                                         ("X","X",None),
                                         (None,None,None))
    assert tetromino.tetromino_color == 'green'
    assert tetromino.tetromino_position == (0, 3)

def test_left_snake():
    """ Test the initialization of the tetrominoes"""
    random.seed(5)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == 'left_snake'
    assert tetromino.tetromino_shape == (("X","X",None),
                                         (None,"X","X"),
                                         (None,None,None))
    assert tetromino.tetromino_color == 'red'
    assert tetromino.tetromino_position == (0, 3)


def test_right_gun():
    """ Test the initialization of the tetrominoes"""
    random.seed(111)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == 'right_gun'
    assert tetromino.tetromino_shape == ((None,None,"X"),
                                         ("X","X","X"),
                                         (None,None,None))
    assert tetromino.tetromino_color == 'orange'
    assert tetromino.tetromino_position == (0, 3)


def test_left_gun():
    """ Test the initialization of the tetrominoes"""
    random.seed(19)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == 'left_gun'
    assert tetromino.tetromino_shape == (("X",None,None),
                                         ("X","X","X"),
                                         (None,None,None))
    assert tetromino.tetromino_color == 'cyan'
    assert tetromino.tetromino_position == (0, 3)


def test_square():
    """ Test the initialization of the tetrominoes"""
    random.seed(1)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == 'square'
    assert tetromino.tetromino_shape == (("X","X"),
                                         ("X","X"))
    assert tetromino.tetromino_color == 'yellow'
    assert tetromino.tetromino_position == (0, 4)


def test_hat():
    """ Test the initialization of the tetrominoes"""
    random.seed(7)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == 'hat'
    assert tetromino.tetromino_shape == ((None,"X",None),
                                         ("X","X","X"),
                                         (None,None,None))
    assert tetromino.tetromino_color == 'pink'
    assert tetromino.tetromino_position == (0, 3)


def test_long():
    """ Test the initialization of the tetrominoes"""
    random.seed(123)
    tetromino = Tetrominoes()
    assert tetromino.tetromino_name == 'long'
    assert tetromino.tetromino_shape ==((None,None,None,None),
                                        ("X","X","X","X"),
                                        (None,None,None,None),
                                        (None,None,None,None))
    assert tetromino.tetromino_color == 'blue'
    assert tetromino.tetromino_position == (0, 3)
