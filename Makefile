# Makefile for tictactoe game dev
# 
# Usage:
#   make api     # run only the Flask server
#   make web     # run only the React dev client
#   make install # install both server + client deps

.PHONY: api web install clean

# paths
CURRENT_DIR := $(shell pwd)
SERVER_DIR=${CURRENT_DIR}/server
CLIENT_DIR=${CURRENT_DIR}/client

# commands
PYTHON=$(SERVER_DIR)/.venv/bin/python
PIP=$(SERVER_DIR)/.venv/bin/pip
NPM=npm

install:
	if ! python3 -m venv --help >/dev/null 2>&1; then \
		cd $(SERVER_DIR) && python3 -m venv .venv && $(PIP) install -r requirements.txt; \
	else \
		cd $(SERVER_DIR) && python3 -m virtualenv .venv && $(PIP) install -r requirements.txt; \
	fi
	if ! $(NPM) --version | awk -F. '{ exit ($$1 < 20) }'; then \
		echo "Node.js version 20 or higher is required."; \
		exit 1; \
	fi
	cd $(CLIENT_DIR) && $(NPM) install

api:
	cd $(SERVER_DIR) && FLASK_APP=app.py FLASK_ENV=development $(PYTHON) -m flask run --port 8000

web:
	cd $(CLIENT_DIR) && $(NPM) run dev -- --port 5173

clean:
	rm -rf $(SERVER_DIR)/.venv $(SERVER_DIR)/__pycache__
	rm -rf $(CLIENT_DIR)/node_modules $(CLIENT_DIR)/dist