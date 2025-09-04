__doc__ = """
Contains the main application logic for the server.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from tictactoe import new_board

app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return {"ok": True}, 200


@app.post("/api/new")
def api_new():
    return jsonify({"board": new_board(), "next": "X"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
