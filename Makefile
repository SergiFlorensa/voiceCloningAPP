SHELL := /usr/bin/env bash

.PHONY: bootstrap backend-install frontend-install backend-dev frontend-dev lint test

bootstrap: backend-install frontend-install

backend-install:
	@echo "==> Installing backend dependencies"
	@cd backend && if command -v uv >/dev/null 2>&1; then \
		uv pip install -e ".[dev]"; \
	else \
		echo "uv not found. Run 'python -m venv .venv && . .venv/bin/activate && pip install -e .[dev]' manually."; \
	fi

frontend-install:
	@echo "==> Installing frontend dependencies"
	@cd frontend && if command -v pnpm >/dev/null 2>&1; then \
		pnpm install; \
	elif command -v npm >/dev/null 2>&1; then \
		npm install; \
	else \
		echo "Neither pnpm nor npm found. Install Node.js tooling and retry."; \
	fi

backend-dev:
	@cd backend && uv run uvicorn app.main:app --reload --port 8000

frontend-dev:
	@cd frontend && npm run dev -- --host

lint:
	@cd backend && uv run ruff check
	@cd frontend && npm run lint

backend-test:
	@cd backend && uv run pytest

test: backend-test
