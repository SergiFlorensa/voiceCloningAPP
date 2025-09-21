from __future__ import annotations

import asyncio
from asyncio.subprocess import DEVNULL, PIPE
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings

_settings = get_settings()
_RAW_DIR = _settings.storage_dir / "incoming"
_NORMALIZED_DIR = _settings.storage_dir / "normalized"

_MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024
_CHUNK_SIZE_BYTES = 1 * 1024 * 1024
_FFMPEG_TIMEOUT_SECONDS = 60

for directory in (_RAW_DIR, _NORMALIZED_DIR):
    directory.mkdir(parents=True, exist_ok=True)


async def save_and_normalize(file: UploadFile) -> Path:
    """Persist the uploaded file and normalize it to 16kHz mono WAV."""
    filename = Path(file.filename or "input")
    ext = filename.suffix.lower() or ".wav"
    identifier = uuid4().hex

    raw_path = _RAW_DIR / f"{identifier}{ext}"
    normalized_path = _NORMALIZED_DIR / f"{identifier}.wav"

    total_bytes = 0

    try:
        with raw_path.open("wb") as buffer:
            while chunk := await file.read(_CHUNK_SIZE_BYTES):
                total_bytes += len(chunk)
                if total_bytes > _MAX_FILE_SIZE_BYTES:
                    raise ValueError("Reference audio exceeds the 20MB limit")
                buffer.write(chunk)

        if total_bytes == 0:
            raise ValueError("Reference audio file is empty")

        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-y",
            "-i",
            str(raw_path),
            "-ac",
            "1",
            "-ar",
            "16000",
            str(normalized_path),
            stdout=DEVNULL,
            stderr=PIPE,
        )

        try:
            _, stderr = await asyncio.wait_for(
                process.communicate(), timeout=_FFMPEG_TIMEOUT_SECONDS
            )
        except asyncio.TimeoutError as exc:  # pragma: no cover - best effort safeguard
            process.kill()
            await process.communicate()
            raise RuntimeError("FFmpeg normalization timed out") from exc

        if process.returncode != 0:
            error_message = "FFmpeg normalization failed"
            if stderr:
                decoded = stderr.decode(errors="ignore").strip()
                if decoded:
                    error_message = f"{error_message}: {decoded}"
            raise RuntimeError(error_message)

        return normalized_path
    except Exception:
        normalized_path.unlink(missing_ok=True)
        raise
    finally:
        raw_path.unlink(missing_ok=True)
