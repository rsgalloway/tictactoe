# Tic‑Tac‑Toe

A monorepo that contains a Tic-Tac-Toe game.

### Architecture

| Feature          | Description |
|------------------|------------------|
| Frontend         | React SPA (Vite) |
| Backend          | Python Flask API, and game logic |
| State            | Server-authoritative. Web client sends moves, server returns updated board |
| Containerization  | Separate Dockerfiles (client/server) |
| Deployment       | ECS Fargate (Not implemented) |

### API Design

Minimal, stateless API using a compact board representation to avoid server
session complexity. The board is a 9-char string, representing positions 0–8:

- empty: "."
- human: "X"
- AI: "O"

So for example, and empty board would be "........."

#### Endpoints

- `GET /health` -> `{ "ok": true }`
- `POST /api/new` -> `{ "board": ".........", next: "X" }`
- `POST /api/move` -> `{
    "aiMove": {
        "index": 4,
        "player": "O"
    },
    "board": "X...O....",
    "lastMove": {
        "index": 0,
        "player": "X"
    },
    "lines": null,
    "status": "playing"
}`

### Minimax

Uses [Minimax](https://en.wikipedia.org/wiki/Minimax#Combinatorial_game_theory)
algorithm (recursive search and scoring) for AI game play. The minimax logic is
implemented in the `tictactoe.py` module and examines every possible move to
determine the next best move. Each position on the board is scored according to a
win/loss/draw (+1/-1/0) for the AI, and the position with the maximum score for
the AI is returned.

## Server

Set up a virtual environment and install requirements:

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest
```

Run the server:

```bash
python3 app.py
```

### Running a health check

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/new
```

### Running tests

```bash
cd server
pytest ./tests
```

### Docker

Building a dev Docker image and running the server app:

```bash
sudo docker build --no-cache -t tictactoe-api:dev .
sudo docker run --rm -p 8000:8000 tictactoe-api:dev
```

## Web client

Install requirements:

```bash
cd client
npm install -D vitest @vitejs/plugin-react @testing-library/react @testing-library/jest-dom
```

Run the web client:

```bash
npm run dev
```

### Docker

Building a dev Docker image and running the client app:

```bash
sudo docker build --no-cache -t tictactoe-web:dev .
sudo docker run --rm -p 5173:5173 -e API_URL=http://localhost:8000 tictactoe-web:dev
```