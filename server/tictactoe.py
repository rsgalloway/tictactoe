__doc__ = """
Contains the Tic-Tac-Toe game logic.

Board is a 9-char string, for example, an empty board: "........."

Board characters:
- empty: "."
- human: "X"
- AI: "O"
"""

from typing import Dict, Optional, Tuple, List

# default board size
BOARD_SIZE: int = 9

# contains all possible winning lines (tuples of board indices)
# TODO: auto-generate this depending on BOARD_SIZE
WINNING_LINES: List[Tuple[int, int, int]] = [
    (0, 1, 2),
    (0, 3, 6),
    (0, 4, 8),
    (1, 4, 7),
    (2, 4, 6),
    (2, 5, 8),
    (3, 4, 5),
    (6, 7, 8),
]


class Chars:
    """Character constants for the board."""

    AI: str = "O"
    EMPTY: str = "."
    HUMAN: str = "X"


class Errors:
    """Error message constants."""

    CELL_OCCUPIED: str = "cell occupied"
    GAME_OVER: str = "game is already over"
    INVALID_BOARD: str = "invalid board"
    INVALID_MOVE_INDEX: str = "invalid move index"
    INVALID_TURN_ORDER: str = "invalid turn order"
    NO_VALID_MOVES: str = "no legal moves"


class Status:
    """Game status constants."""

    DRAW: str = "draw"
    PLAYING: str = "playing"
    O_WON: str = "o_won"
    X_WON: str = "x_won"


# stores board evaluations to speed up minimax
_CACHE: Dict[str, Tuple[int, int]] = {}


# TODO: support different board sizes (4x4, 5x5, 6x6, etc.)
def new_board(size: int = BOARD_SIZE) -> str:
    """Create a new empty board.

    :param size: size of the board, default 9.
    :return: 9-char string representing the board.
    """
    global BOARD_SIZE
    BOARD_SIZE = size
    return Chars.EMPTY * size


def is_terminal(board: str) -> Tuple[str, Optional[List[int]]]:
    """Return (status, winning_line_or_None).

    :param board: 9-char string representing the board.
    :return: (status, winning_line_or_None)
    """
    b = board
    assert isinstance(b, str) and len(b) == BOARD_SIZE, Errors.INVALID_BOARD

    for a, b1, c in WINNING_LINES:
        trio = board[a] + board[b1] + board[c]
        if trio == Chars.HUMAN * int(BOARD_SIZE**0.5):
            return Status.X_WON, [a, b1, c]
        if trio == Chars.AI * int(BOARD_SIZE**0.5):
            return Status.O_WON, [a, b1, c]

    # if no empty cells, it's a draw
    if Chars.EMPTY not in board:
        return Status.DRAW, None

    return Status.PLAYING, None


def apply_move(board: str, idx: int, mark: str) -> str:
    """Apply a move to the board and return the new board string.

    :param board: 9-char string representing the board.
    :param idx: index (0-8) to place the mark.
    :param mark: either Chars.HUMAN ('X') or Chars.AI ('O').
    :return: new board string with the move applied.
    """
    assert mark in (Chars.HUMAN, Chars.AI)
    return board[:idx] + mark + board[idx + 1 :]


def _next_player(board: str) -> str:
    """Whose turn is it given board counts? Human (X) always starts.

    :param board: 9-char string representing the board.
    :return: Chars.HUMAN or Chars.AI
    """
    x = board.count(Chars.HUMAN)
    o = board.count(Chars.AI)
    return Chars.HUMAN if x == o else Chars.AI


def _score_terminal(status: str) -> int:
    """Score from AI ('O') perspective.

    :param status: game status string.
    :return: +1 if AI won, -1 if human won, 0 if draw.
    """
    if status == Status.O_WON:
        return +1
    if status == Status.X_WON:
        return -1
    return 0


def _available_moves(board: str) -> List[int]:
    """Return list of available move indices. Iterates left to right, top to bottom.

    :param board: 9-char string representing the board.
    :return: list of indices (0-8) that are empty.
    """
    return [i for i, ch in enumerate(board) if ch == Chars.EMPTY]


def _winning_moves(board: str, player: str) -> List[int]:
    """Return list of immediate winning move indices for the given player.
    Iterates over the current board and looks for moves that would result in an
    immediate win for example: XO..OX.OX.

    :param board: 9-char string representing the board.
    :param player: either Chars.HUMAN or Chars.AI.
    :return: list of indices (0-8) that would result in an immediate win for the player.
    """
    wins = []
    for i, ch in enumerate(board):
        if ch == Chars.EMPTY:
            nb = apply_move(board, i, player)
            status, _ = is_terminal(nb)
            if (player == Chars.AI and status == Status.O_WON) or (
                player == Chars.HUMAN and status == Status.X_WON
            ):
                wins.append(i)
    return wins


def validate_move(board: str, idx: Optional[int]) -> Tuple[bool, str]:
    """Validate a proposed move.

    :param board: 9-char string representing the board.
    :param idx: index (0-8) for the proposed move.
    :return: (is_valid, error_message). If is_valid is True, error_message is empty.
    :raises AssertionError: if board is invalid or idx is invalid.
    """
    if not isinstance(board, str) or len(board) != BOARD_SIZE:
        return False, Errors.INVALID_BOARD

    if idx is None or not isinstance(idx, int) or not (0 <= idx <= BOARD_SIZE - 1):
        return False, Errors.INVALID_MOVE_INDEX

    status, _ = is_terminal(board)

    if status != Status.PLAYING:
        return False, Errors.GAME_OVER

    if board[idx] != Chars.EMPTY:
        return False, Errors.CELL_OCCUPIED

    # human must be first mover
    if board.count(Chars.HUMAN) < board.count(Chars.AI):
        return False, Errors.INVALID_TURN_ORDER

    return True, ""


def _minimax(board: str, player: str, alpha: int, beta: int) -> Tuple[int, int]:
    """
    Implements minimax with alpha-beta pruning.

    Return (best_index, best_score) from current player's perspective, where score
    is always from AI ('O') perspective.

    :param board: current board state
    :param player: current player to move, either Chars.HUMAN or Chars.AI
    :param alpha: alpha value for alpha-beta pruning
    :param beta: beta value for alpha-beta pruning
    :return: (best_index, best_score)
    :raises AssertionError: if board is invalid or player is invalid
    """
    status, _ = is_terminal(board)

    # terminal position
    if status != Status.PLAYING or player not in (Chars.HUMAN, Chars.AI):
        return -1, _score_terminal(status)

    # check for cache hits
    cache_hit = _CACHE.get(board)
    if cache_hit is not None:
        return cache_hit

    # get all available moves
    moves = _available_moves(board)

    # AI player, maximizing
    if player == Chars.AI:
        best_idx = moves[0]
        best_val = -2  # < worst possible
        for idx in moves:
            child = apply_move(board, idx, Chars.AI)
            _, val = _minimax(child, Chars.HUMAN, alpha, beta)
            if val > best_val:
                best_val, best_idx = val, idx
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        _CACHE[board] = (best_idx, best_val)
        return best_idx, best_val

    # human player, minimizing
    else:
        worst_idx = moves[0]
        worst_val = +2  # > best possible
        for idx in moves:
            child = apply_move(board, idx, Chars.HUMAN)
            _, val = _minimax(child, Chars.AI, alpha, beta)
            if val < worst_val:
                worst_val, worst_idx = val, idx
            beta = min(beta, worst_val)
            if beta <= alpha:
                break
        _CACHE[board] = (worst_idx, worst_val)
        return worst_idx, worst_val


# TODO: optionally predict outcome if only one empty cell remains
def best_ai_reply(board: str) -> int:
    """
    Return optimal index for AI ('O').

    :param board: current board state
    :return: index (0-8) for AI's move
    :raises RuntimeError: if no valid moves are available or game is over
    """
    status, _ = is_terminal(board)

    # make sure game is still running
    if status != Status.PLAYING:
        raise RuntimeError(Errors.NO_VALID_MOVES)

    # look for immediate win (i.e. win in one move)
    # TODO: deterministic preference (e.g. center, corners, sides)
    immediate = _winning_moves(board, Chars.AI)
    if immediate:
        return immediate[0]

    # make sure it's AI's turn
    player = _next_player(board)
    if player != Chars.AI:
        # simulate all human moves and pick the best one for AI
        best_choice = None
        best_val = -2
        for idx in _available_moves(board):
            child = apply_move(board, idx, Chars.HUMAN)
            ai_idx, val = _minimax(child, Chars.AI, alpha=-2, beta=+2)
            # maximize AI score
            if val > best_val:
                best_val = val
                best_choice = ai_idx
        if best_choice is None:
            raise RuntimeError(Errors.NO_VALID_MOVES)
        return best_choice

    # run minimax
    idx, _ = _minimax(board, Chars.AI, alpha=-2, beta=+2)
    if idx is None or idx < 0:
        raise RuntimeError(Errors.NO_VALID_MOVES)

    return idx
