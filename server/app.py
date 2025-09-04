__doc__ = """
Contains the main application logic for the server.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from tictactoe import (
    Chars,
    Status,
    new_board,
    is_terminal,
    apply_move,
    best_ai_reply,
    validate_move,
)

# Flask app setup
app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"ok": True}, 200


@app.post("/api/new")
def api_new():
    """Start a new game."""
    return jsonify({"board": new_board(), "next": Chars.HUMAN})


@app.post("/api/move")
def api_move():
    """Process a player's move and return the updated game state."""
    data = request.get_json(force=True)
    board: str = data.get("board", "")
    move = data.get("move", None)

    # validate the move
    ok, err = validate_move(board, move)
    if not ok:
        return jsonify({"error": err}), 400

    # apply the move from the human player and...
    board = apply_move(board, move, Chars.HUMAN)
    status, line = is_terminal(board)
    last = {"player": Chars.HUMAN, "index": move}

    # ...check if the game is over, return the result
    if status != Status.PLAYING:
        return jsonify(
            {"board": board, "status": status, "lastMove": last, "lines": line}
        )

    # if not over, apply the move from the AI player
    ai_index = best_ai_reply(board)
    board = apply_move(board, ai_index, Chars.AI)
    status, line = is_terminal(board)

    return jsonify(
        {
            "board": board,
            "status": status,
            "lastMove": last,
            "aiMove": {"player": Chars.AI, "index": ai_index},
            "lines": line,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
