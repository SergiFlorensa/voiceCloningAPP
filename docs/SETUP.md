# Development Setup

This guide walks through preparing the project for local development.

## Prerequisites

- Python 3.10 or 3.11
- Node.js 20+
- FFmpeg available in `PATH`
- (Optional) `uv` for faster Python dependency management
- (Optional) `pnpm` for faster JavaScript installs

## Bootstrap

You can bootstrap everything with the provided script:

```bash
scripts/bootstrap.sh
```

On Windows PowerShell:

```powershell
scripts\bootstrap.ps1
```

The script installs backend dependencies (preferring `uv`) and frontend dependencies (preferring `pnpm`).

## Environment variables

Copy the sample files and adjust as needed:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

## Useful commands

- `make bootstrap` - install backend + frontend deps
- `make backend-dev` - launch FastAPI with auto-reload on port 8000
- `make frontend-dev` - start Vite dev server on port 5173
- `make lint` - run backend Ruff checks and frontend ESLint
- `make test` - execute backend pytest suite

These commands assume you have `make` available. You can also run the underlying `uv`/`npm` commands directly if you prefer.
