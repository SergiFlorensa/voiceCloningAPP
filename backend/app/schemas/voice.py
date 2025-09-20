from __future__ import annotations

from pydantic import BaseModel, Field


class VoiceCloneResponse(BaseModel):
    ok: bool = Field(default=True, description="Indicates whether the cloning succeeded")
    download_url: str = Field(description="Public URL to retrieve the generated audio")


class HealthResponse(BaseModel):
    ok: bool = Field(default=True, description="API status flag")
    environment: str = Field(description="Current runtime environment identifier")
