from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.core.config import get_settings

try:
    from TTS.api import TTS as CoquiTTS
except ImportError:  # pragma: no cover - optional heavy dependency
    CoquiTTS = None  # type: ignore[assignment]

_settings = get_settings()
_OUTPUT_DIR = _settings.storage_dir / "generated"
_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

_TORCH_SERIALIZATION_CONFIGURED = False


def _ensure_torch_safe_globals() -> None:
    """Allow torch.load to restore Coqui XTTS configs on PyTorch >=2.6."""
    global _TORCH_SERIALIZATION_CONFIGURED
    if _TORCH_SERIALIZATION_CONFIGURED:
        return
    try:
        from torch.serialization import add_safe_globals  # type: ignore[import]
        from TTS.tts.configs.xtts_config import XttsConfig  # type: ignore[import]
    except Exception:
        return
    try:
        add_safe_globals([XttsConfig])
    except Exception:
        return
    _TORCH_SERIALIZATION_CONFIGURED = True


_TTS_TIMEOUT_SECONDS = 180

_tts_model: Any | None = None


def _get_model() -> Any:
    """Load the TTS model once and reuse the instance."""
    global _tts_model
    if _tts_model is None:
        if CoquiTTS is None:  # pragma: no cover - optional heavy dependency
            raise RuntimeError(
                "The 'TTS' package is not installed. Install it (and PyTorch) to enable voice synthesis."
            )
        _ensure_torch_safe_globals()
        _tts_model = CoquiTTS(model_name=_settings.tts_model_name)
    return _tts_model


async def synthesize_voice(text: str, reference_path: Path) -> Path:
    """Generate a voice clip cloning the provided reference."""
    tts = _get_model()
    output_path = _OUTPUT_DIR / f"voice-{uuid4().hex}.wav"

    try:
        await asyncio.wait_for(
            asyncio.to_thread(
                tts.tts_to_file,
                text=text,
                speaker_wav=str(reference_path),
                file_path=str(output_path),
            ),
            timeout=_TTS_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError as exc:  # pragma: no cover - best effort safeguard
        output_path.unlink(missing_ok=True)
        raise RuntimeError("Voice synthesis timed out") from exc
    except Exception:
        output_path.unlink(missing_ok=True)
        raise

    return output_path
