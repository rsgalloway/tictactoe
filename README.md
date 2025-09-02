# Tic‑Tac‑Toe

A monorepo that contains an unbeatable Tic-Tac-Toe game.

## server

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest
python3 app.py
```

Building a dev Docker image and running the server app:

```bash
sudo docker build -t tictactoe-api:dev .
sudo docker run --rm -p 8000:8000 tictactoe-api:dev
```

## client

```bash
cd client
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

Building a dev Docker image and running the client app:

```bash
sudo docker build -t tictactoe-web:dev .
sudo docker run --rm -p 3000:3000 tictactoe-web:dev
```