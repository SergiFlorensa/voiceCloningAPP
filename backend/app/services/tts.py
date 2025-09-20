from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from TTS.api import TTS

from app.core.config import get_settings

_settings = get_settings()
_OUTPUT_DIR = _settings.storage_dir / "generated"
_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

_tts_model: TTS | None = None


def _get_model() -> TTS:
    """Load the TTS model once and reuse the instance."""
    global _tts_model
    if _tts_model is None:
        _tts_model = TTS(model_name=_settings.tts_model_name)
    return _tts_model


async def synthesize_voice(text: str, reference_path: Path) -> Path:
    """Generate a voice clip cloning the provided reference."""
    tts = _get_model()
    output_path = _OUTPUT_DIR / f"voice-{uuid4().hex}.wav"
    tts.tts_to_file(text=text, speaker_wav=str(reference_path), file_path=str(output_path))
    return output_path
