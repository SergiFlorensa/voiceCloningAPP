# Voice Cloning Backend

This directory contains the FastAPI backend for the Voice Cloning application. It exposes
REST endpoints to accept reference audio, normalise it with FFmpeg, and generate cloned speech
using the Coqui XTTS v2 model.

## Development

```bash
uv venv
uv pip install -e .
uv run uvicorn app.main:app --reload
```

Replace `uv` with your preferred package manager (`pip`, `poetry`, etc.) if needed.
