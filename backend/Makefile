.PHONY: help install install-dev run test test-one curl-sh curl-py

PY ?= python3
PIP ?= pip3
UVICORN ?= uvicorn
APP ?= app.main:app
HOST ?= 0.0.0.0
PORT ?= 8000
LOG_LEVEL ?= debug

help:
	@echo "Targets:"
	@echo "  install       Install runtime and dev dependencies (requirements.txt)"
	@echo "  install-dev   Editable install via pyproject.toml (pip install -e .)"
	@echo "  run           Start FastAPI dev server with uvicorn"
	@echo "  test          Run backend tests with pytest"
	@echo "  test-one      Run a single test (usage: make test-one FILE=tests/test_optimization.py)"
	@echo "  curl-sh       Run curl smoke tests (server must be running)"
	@echo "  curl-py       Run Python smoke tests (server must be running)"

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -e .

run:
	$(UVICORN) $(APP) --reload --host $(HOST) --port $(PORT) --log-level $(LOG_LEVEL)

# pytest.ini config sets pythonpath=app
test:
	$(PY) -m pytest -q

# Usage: make test-one FILE=tests/test_optimization.py
FILE ?= tests/test_optimization.py

test-one:
	$(PY) -m pytest -q $(FILE)

curl-sh:
	./scripts/test_with_curl.sh

curl-py:
	$(PY) scripts/test_with_curl.py

