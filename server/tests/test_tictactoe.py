__doc__ = """
Contains the tests for the tictactoe.py module.
"""

import pytest

from ..tictactoe import (
    Chars,
    Errors,
    Status,
    new_board,
    is_terminal,
    apply_move,
    validate_move,
    best_ai_reply,
)


def B(s: str) -> str:
    """Helper to validate board strings in tests."""
    assert len(s) == 9, "board must be 9 chars"
    return s


WIN_CASES = [
    ("XXX......", "x_won", [0, 1, 2]),
    ("...XXX...", "x_won", [3, 4, 5]),
    ("......XXX", "x_won", [6, 7, 8]),
    ("X..X..X..", "x_won", [0, 3, 6]),
    (".X..X..X.", "x_won", [1, 4, 7]),
    ("..X..X..X", "x_won", [2, 5, 8]),
    ("O..O..O..", "o_won", [0, 3, 6]),
    ("OOO......", "o_won", [0, 1, 2]),
    ("O...O...O", "o_won", [0, 4, 8]),
    ("..O.O.O..", "o_won", [2, 4, 6]),
]


def test_new_board_is_empty():
    """Test that new_board() creates an empty board."""
    assert new_board() == Chars.EMPTY * 9


def test_terminal_detection():
    """Basic test that is_terminal() detects wins and draws."""
    b = "XXX......"
    status, line = is_terminal(b)
    assert status == Status.X_WON and set(line) == {0, 1, 2}

    b = "OOO......"
    status, line = is_terminal(b)
    assert status == Status.O_WON and set(line) == {0, 1, 2}

    b = "XOXOOXXXO"
    status, _ = is_terminal(b)
    assert status in {
        Status.DRAW,
        Status.X_WON,
    }


@pytest.mark.parametrize("board,expected,line", WIN_CASES)
def test_is_terminal_wins(board, expected, line):
    status, winning = is_terminal(B(board))
    assert status == expected
    if winning:
        assert set(winning) == set(line)


def test_is_terminal_draw():
    """known draw (no three-in-a-row)"""
    board = B("XOXOXOOXO")
    status, line = is_terminal(board)
    assert status == Status.DRAW
    assert line is None


def test_is_terminal_playing():
    """Test a non-terminal board."""
    board = B("X........")
    status, line = is_terminal(board)
    assert status == Status.PLAYING
    assert line is None


def test_apply_move_and_validate_ok():
    """Test that validate_move() accepts a legal move and applies it."""
    board = new_board()
    ok, err = validate_move(board, 0)
    assert ok and not err
    after = apply_move(board, 0, Chars.HUMAN)
    assert after == Chars.HUMAN + Chars.EMPTY * 8


def test_validate_move_rejects_occupied():
    """Test that validate_move() rejects moves to occupied cells."""
    board = apply_move(new_board(), 0, Chars.HUMAN)
    ok, err = validate_move(board, 0)
    assert not ok and "occupied" in err


def test_validate_move_rejects_invalid_index():
    """Test that validate_move() rejects out-of-bounds indices."""
    board = new_board()
    ok, _ = validate_move(board, -1)
    assert not ok
    ok, _ = validate_move(board, 9)
    assert not ok


def test_validate_move_rejects_after_terminal():
    """Test that validate_move() rejects moves after game over."""
    board = B("XXX......")
    ok, err = validate_move(board, 3)
    assert not ok and "already over" in err


def test_validate_move_turn_order():
    """Test that validate_move() enforces turn order."""
    board = B("O........")
    ok, err = validate_move(board, 1)
    assert not ok and str(err) == Errors.INVALID_TURN_ORDER


def test_ai_blocks_immediate_win_by_x():
    """Test that best_ai_reply() blocks an immediate win by X."""
    board = B("XX....O..")
    idx = best_ai_reply(board)
    assert idx == 2


def test_ai_raises_when_no_moves_left():
    """Test that best_ai_reply() raises when no moves are possible."""
    board = B("XOXOOXXXO")
    with pytest.raises(RuntimeError) as e:
        best_ai_reply(board)
    assert Errors.NO_VALID_MOVES in str(e.value)
