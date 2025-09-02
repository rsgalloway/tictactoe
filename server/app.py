__doc__ = """
Contains the main application logic for the server.
"""

from flask import Flask

app = Flask(__name__)


@app.get("/health")
def health():
    return {"ok": True}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
