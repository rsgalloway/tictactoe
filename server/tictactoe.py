__doc__ = """
Contains the Tic-Tac-Toe game logic.

Board is a 9-char string, for example, an empty board: "........."

- empty: "."
- human: "X"
- AI: "O"
"""

from typing import Optional, Tuple, List

# board characters
CHAR_EMPTY = "."
CHAR_HUMAN = "X"
CHAR_AI = "O"

# default board size
BOARD_SIZE = 9

# contains all possible winning lines (tuples of board indices)
# TODO: auto-generate this depending on BOARD_SIZE
WINNING_LINES = [
    (0, 1, 2),
    (0, 3, 6),
    (0, 4, 8),
    (1, 4, 7),
    (2, 4, 6),
    (2, 5, 8),
    (3, 4, 5),
    (6, 7, 8),
]


class Errors:
    """Error message constants."""
    CELL_OCCUPIED = "cell occupied"
    GAME_OVER = "game is already over"
    INVALID_BOARD = "invalid board"
    INVALID_MOVE_INDEX = "invalid move index"
    INVALID_TURN_ORDER = "invalid turn order"
    NO_VALID_MOVES = "no legal moves"


class Status:
    """Game status constants."""
    DRAW = "draw"
    PLAYING = "playing"
    O_WON = "o_won"
    X_WON = "x_won"


def new_board(size: int = BOARD_SIZE) -> str:
    """Create a new empty board.

    :param size: size of the board, default 9.
    :return: 9-char string representing the board.
    """
    global BOARD_SIZE
    BOARD_SIZE = size
    return CHAR_EMPTY * size


def is_terminal(board: str) -> Tuple[str, Optional[List[int]]]:
    """Return (status, winning_line_or_None).

    :param board: 9-char string representing the board.
    :return: (status, winning_line_or_None)
    """
    b = board
    assert isinstance(b, str) and len(b) == BOARD_SIZE, Errors.INVALID_BOARD

    for a, b1, c in WINNING_LINES:
        trio = board[a] + board[b1] + board[c]
        if trio == CHAR_HUMAN * int(BOARD_SIZE**0.5):
            return Status.X_WON, [a, b1, c]
        if trio == CHAR_AI * int(BOARD_SIZE**0.5):
            return Status.O_WON, [a, b1, c]

    # if no empty cells, it's a draw
    if CHAR_EMPTY not in board:
        return Status.DRAW, None

    return Status.PLAYING, None


def apply_move(board: str, idx: int, mark: str) -> str:
    """Apply a move to the board and return the new board string.

    :param board: 9-char string representing the board.
    :param idx: index (0-8) to place the mark.
    :param mark: either CHAR_HUMAN ('X') or CHAR_AI ('O').
    :return: new board string with the move applied.
    """
    assert mark in (CHAR_HUMAN, CHAR_AI)
    return board[:idx] + mark + board[idx + 1 :]


def validate_move(board: str, idx: Optional[int]) -> Tuple[bool, str]:
    """Validate a proposed move.

    :param board: 9-char string representing the board.
    :param idx: index (0-8) for the proposed move.
    :return: (is_valid, error_message). If is_valid is True, error_message is empty.
    """
    if not isinstance(board, str) or len(board) != BOARD_SIZE:
        return False, Errors.INVALID_BOARD

    if idx is None or not isinstance(idx, int) or not (0 <= idx <= BOARD_SIZE - 1):
        return False, Errors.INVALID_MOVE_INDEX

    status, _ = is_terminal(board)

    if status != Status.PLAYING:
        return False, Errors.GAME_OVER

    if board[idx] != CHAR_EMPTY:
        return False, Errors.CELL_OCCUPIED

    # human must be first mover
    if board.count(CHAR_HUMAN) < board.count(CHAR_AI):
        return False, Errors.INVALID_TURN_ORDER

    return True, ""


# TODO: implement minimax + alpha-beta pruning
def best_ai_reply(board: str) -> int:
    """Return optimal index for AI ('O'). Placeholder picks first empty cell until implemented.

    :param board: 9-char string representing the board.
    :return: index (0-8) for AI's move.
    """
    for i, ch in enumerate(board):
        if ch == CHAR_EMPTY:
            return i
    raise RuntimeError(Errors.NO_VALID_MOVES)
