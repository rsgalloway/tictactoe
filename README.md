# Tic‑Tac‑Toe

A monorepo that contains a Tic-Tac-Toe game.

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