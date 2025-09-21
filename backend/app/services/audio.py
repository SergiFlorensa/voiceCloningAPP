from __future__ import annotations

import asyncio
import subprocess
from pathlib import Path
from typing import Callable
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


def _build_ffmpeg_runner(args: list[str]) -> Callable[[], subprocess.CompletedProcess[bytes]]:
    creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

    def _runner() -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=False,
            creationflags=creation_flags,
        )

    return _runner


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

        ffmpeg_bin = str(_settings.ffmpeg_bin)
        args = [
            ffmpeg_bin,
            "-y",
            "-i",
            str(raw_path),
            "-ac",
            "1",
            "-ar",
            "16000",
            str(normalized_path),
        ]

        loop = asyncio.get_running_loop()
        runner = _build_ffmpeg_runner(args)

        try:
            completed = await asyncio.wait_for(
                loop.run_in_executor(None, runner),
                timeout=_FFMPEG_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError as exc:  # pragma: no cover
            raise RuntimeError("FFmpeg normalization timed out") from exc

        if completed.returncode != 0:
            error_message = "FFmpeg normalization failed"
            if completed.stderr:
                decoded = completed.stderr.decode(errors="ignore").strip()
                if decoded:
                    error_message = f"{error_message}: {decoded}"
            raise RuntimeError(error_message)

        return normalized_path
    except Exception:
        normalized_path.unlink(missing_ok=True)
        raise
    finally:
        raw_path.unlink(missing_ok=True)

