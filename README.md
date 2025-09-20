# Voice Cloning App

Personal project inspired by NoteGPT's voice cloning flow. Upload a short audio/video
sample, provide any text, and let the backend generate a new clip using the same voice via
Coqui XTTS v2.

## Features

- Audio/video upload with automatic normalisation (FFmpeg -> 16 kHz mono WAV)
- Text-to-speech generation with speaker cloning (XTTS v2)
- React frontend with form validation, progress feedback, and audio preview
- FastAPI backend exposing REST endpoints and serving generated files
- Docker Compose stack for local deployment with persistent volumes

## Tech Stack

| Layer     | Technologies |
|-----------|--------------|
| Frontend  | React 19, Vite, TypeScript, Tailwind CSS v4, React Query, React Hook Form |
| Backend   | Python 3.11, FastAPI, Uvicorn, Pydantic, Coqui TTS (XTTS v2) |
| Tooling   | uv / pip, npm / pnpm, Ruff, Pytest, ESLint, Docker, FFmpeg |

## Repository Layout

```
backend/        # FastAPI application (app/, services/, schemas/, tests/)
frontend/       # React app organised by feature modules
infrastructure/ # Dockerfiles, nginx config, compose stack
scripts/        # Bootstrap helpers for dependency installation
docs/           # Architecture and setup documentation
```

## Getting Started

1. Install prerequisites (Python 3.10+, Node.js 20+, FFmpeg). Optional: `uv`, `pnpm`.
2. Copy environment samples and adjust values:
   ```bash
   cp .env.example .env
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```
3. Bootstrap dependencies:
   ```bash
   make bootstrap
   ```
4. Run services locally:
   ```bash
   make backend-dev    # http://localhost:8000
   make frontend-dev   # http://localhost:5173
   ```

For more detail, see `docs/SETUP.md` and `docs/ARCHITECTURE.md`.

## Docker Compose

Build and run the full stack:

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

Volumes persist generated audio (`backend_storage`) and model downloads
(`backend_model_cache`).

## Roadmap

- [x] CI pipelines (lint, tests, type checks)
- [ ] Voice generation progress feedback and error states in UI
- [ ] Optional GPU-enabled image for faster inference
- [ ] Authentication / rate limiting if opened beyond personal use

> **Note:** Use responsibly. Disclose when audio was generated with AI and respect
> voice ownership rights.
