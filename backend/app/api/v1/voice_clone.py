from __future__ import annotations

import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.schemas.voice import VoiceCloneResponse
from app.services.audio import save_and_normalize
from app.services.tts import synthesize_voice

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice-clone", tags=["voice-clone"])


@router.post("/generate", response_model=VoiceCloneResponse, status_code=status.HTTP_201_CREATED)
async def generate_voice(text: str = Form(...), reference: UploadFile = File(...)) -> VoiceCloneResponse:
    settings = get_settings()

    try:
        normalized_path = await save_and_normalize(reference)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to process reference audio")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error processing reference audio") from exc

    try:
        generated_path = await synthesize_voice(text=text, reference_path=normalized_path)
    except Exception as exc:  # noqa: BLE001
        logger.exception("TTS generation failed")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Voice synthesis failed") from exc

    download_url = _build_download_url(generated_path.name, settings.api_prefix, settings.api_version)
    return VoiceCloneResponse(download_url=download_url)


def _build_download_url(filename: str, api_prefix: str, api_version: str) -> str:
    base = f"{api_prefix}/{api_version}/files"
    return f"{base}/{filename}"
