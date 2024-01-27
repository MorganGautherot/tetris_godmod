from src.score import Score


def test_score_initialization():
    """
    Test the initialization of the score class
    """
    game_score = Score()

    assert game_score.level == 1
    assert game_score.score == 0
    assert game_score.lines == 0
    assert game_score.combo == 1


def test_mark_score():
    """
    Test mak score function
    """
    game_score = Score()

    game_score.mark_score(4)

    assert game_score.level == 1
    assert game_score.score == 1200
    assert game_score.lines == 4
    assert game_score.combo == 2


def test_mark_score_new_level():
    """
    Test mak score function
    """
    game_score = Score()

    game_score.mark_score(15)

    assert game_score.level == 2


def test_reset_combo():
    """
    Test reset combo score
    """
    game_score = Score()
    game_score.combo = 5
    game_score.reset_combo()

    assert game_score.combo == 1
