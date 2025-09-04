__doc__ = """
Contains the tests for the tictactoe.py module.
"""

from tictactoe import is_terminal, new_board


def test_new_board_empty():
    assert new_board() == "........."


def test_terminal_detection():
    b = "XXX......"
    status, line = is_terminal(b)
    assert status == "x_won" and set(line) == {0, 1, 2}

    b = "OOO......"
    status, line = is_terminal(b)
    assert status == "o_won" and set(line) == {0, 1, 2}

    b = "XOXOOXXXO"
    status, _ = is_terminal(b)
    assert status in {"draw", "x_won", "o_won"}
