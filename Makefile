.PHONY: help backend-install backend-install-dev backend-run backend-test backend-test-one backend-curl-sh backend-curl-py \
        frontend-install frontend-start frontend-build frontend-test frontend-test-one

# Root Makefile that proxies to backend/ and frontend/

# Frontend mode: production (default) or debug
MODE ?= production
FRONTEND_DIR := frontend/$(MODE)

help:
	@echo "Root targets:"
	@echo "  backend-install        Install backend deps (requirements.txt)"
	@echo "  backend-install-dev    Editable install via pyproject (pip install -e .)"
	@echo "  backend-run            Start FastAPI dev server"
	@echo "  backend-test           Run backend tests with pytest"
	@echo "  backend-test-one       Run a single backend test (FILE=tests/test_optimization.py)"
	@echo "  backend-curl-sh        Run backend curl smoke tests (server must be running)"
	@echo "  backend-curl-py        Run backend Python smoke tests (server must be running)"
	@echo "  frontend-install       npm install in $(FRONTEND_DIR) (override with MODE=debug)"
	@echo "  frontend-start         npm start in $(FRONTEND_DIR)"
	@echo "  frontend-build         npm run build in $(FRONTEND_DIR)"
	@echo "  frontend-test          npm test (watch mode) in $(FRONTEND_DIR)"
	@echo "  frontend-test-one      npm test single (TEST=App.test.tsx or PATTERN via -t) in $(FRONTEND_DIR)"

# -------- Backend proxies --------
backend-install:
	$(MAKE) -C backend install

backend-install-dev:
	$(MAKE) -C backend install-dev

backend-run:
	$(MAKE) -C backend run

backend-test:
	$(MAKE) -C backend test

# Usage: make backend-test-one FILE=tests/test_optimization.py
backend-test-one:
	$(MAKE) -C backend test-one FILE="$(FILE)"

backend-curl-sh:
	$(MAKE) -C backend curl-sh

backend-curl-py:
	$(MAKE) -C backend curl-py

# -------- Frontend proxies --------
frontend-install:
	cd $(FRONTEND_DIR) && npm install

frontend-start:
	cd $(FRONTEND_DIR) && npm start

frontend-build:
	cd $(FRONTEND_DIR) && npm run build

frontend-test:
	cd $(FRONTEND_DIR) && npm test

# Usage examples:
#   make frontend-test-one TEST=App.test.tsx
#   make frontend-test-one PATTERN="learn react"
frontend-test-one:
	cd $(FRONTEND_DIR) && if [ -n "$(TEST)" ]; then npm test -- "$(TEST)" ; \
	elif [ -n "$(PATTERN)" ]; then npm test -- -t "$(PATTERN)" ; \
	else npm test ; fi

