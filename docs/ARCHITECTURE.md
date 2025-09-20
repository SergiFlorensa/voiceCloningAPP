# Architecture Overview

This document summarises the high-level design of the Voice Cloning App.

## Components

- **Frontend (React + Vite)**
  - User interface for uploading audio, entering text, and downloading results.
  - Talks to the backend through the REST API (`/api/v1`).
  - Built as a static bundle delivered by Nginx when running in containers.

- **Backend (FastAPI)**
  - Exposes health checks and the voice cloning endpoint.
  - Handles audio normalisation with FFmpeg and triggers the XTTS v2 model via `TTS`.
  - Stores temporary artefacts under `/storage` (incoming, normalized, generated).

- **Model Cache**
  - Keeps downloaded model weights to avoid repeated downloads per container restart.
  - Mounted as a dedicated volume (`backend_model_cache`).

- **Volumes and Data**
  - `backend_storage`: persists uploaded and generated audio files.
  - `backend_model_cache`: persists model checkpoints.

## Runtime Flow

1. The frontend submits a multipart request (`text`, `reference` file) to `POST /api/v1/voice-clone/generate`.
2. The backend saves the raw file, normalises it to WAV 16 kHz mono, and caches it in `/storage/normalized`.
3. XTTS v2 consumes the normalised sample, clones the timbre, and writes the output to `/storage/generated`.
4. The backend returns a download URL pointing to the static files mount (`/api/v1/files/{id}.wav`).
5. The frontend presents an audio preview and provides a direct download link.

## Configuration

- Environment variables (root `.env`, `backend/.env`, `frontend/.env`) control ports, API base URL, storage paths, and logging.
- CORS origins default to `http://localhost:5173` for local development.
- FFmpeg must be available on the backend host or container image.

## Deployment with Docker Compose

The `infrastructure/docker-compose.yml` stack provides two services:

| Service  | Port | Description                      |
|----------|------|----------------------------------|
| backend  | 8000 | FastAPI app served by Uvicorn    |
| frontend | 5173 | Static frontend served by Nginx  |

Run the stack (after creating `.env` files) with:

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

## Next Steps

- Introduce a task queue if long-running inference needs to be offloaded.
- Add authentication and rate limiting if the project becomes multi-user.
- Consider storing artefacts in S3/MinIO once deployments move beyond local setups.
