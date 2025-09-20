from __future__ import annotations

import subprocess
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings

_settings = get_settings()
_RAW_DIR = _settings.storage_dir / "incoming"
_NORMALIZED_DIR = _settings.storage_dir / "normalized"

for directory in (_RAW_DIR, _NORMALIZED_DIR):
    directory.mkdir(parents=True, exist_ok=True)


async def save_and_normalize(file: UploadFile) -> Path:
    """Persist the uploaded file and normalize it to 16kHz mono WAV."""
    filename = Path(file.filename or "input")
    ext = filename.suffix.lower() or ".wav"
    identifier = uuid4().hex

    raw_path = _RAW_DIR / f"{identifier}{ext}"
    normalized_path = _NORMALIZED_DIR / f"{identifier}.wav"

    raw_path.write_bytes(await file.read())

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(raw_path),
        "-ac", "1",
        "-ar", "16000",
        str(normalized_path),
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return normalized_path
