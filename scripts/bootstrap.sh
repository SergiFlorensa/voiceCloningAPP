#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

info() {
  printf "\033[1;34m==>\033[0m %s\n" "$1"
}

warn() {
  printf "\033[1;33m[warn]\033[0m %s\n" "$1"
}

info "Installing backend dependencies"
if command -v uv >/dev/null 2>&1; then
  (cd "$ROOT_DIR/backend" && uv pip install -e ".[dev]")
else
  warn "uv not found. Install it from https://github.com/astral-sh/uv or run manually:"
  warn "  cd backend && python -m venv .venv && source .venv/bin/activate && pip install -e '.[dev]'"
fi

info "Installing frontend dependencies"
if command -v pnpm >/dev/null 2>&1; then
  (cd "$ROOT_DIR/frontend" && pnpm install)
elif command -v npm >/dev/null 2>&1; then
  (cd "$ROOT_DIR/frontend" && npm install)
else
  warn "Neither pnpm nor npm found. Install Node.js 20+ to continue."
fi
