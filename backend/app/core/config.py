from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "Voice Cloning API"
    environment: str = "local"
    api_prefix: str = "/api"
    api_version: str = "v1"
    cors_origins: list[str] = ["http://localhost:5173"]
    storage_dir: Path = Path(__file__).resolve().parents[2] / "storage"
    model_cache_dir: Path = Path(__file__).resolve().parents[2] / "model_cache"
    tts_model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    ffmpeg_bin: str = "ffmpeg"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("storage_dir", "model_cache_dir", mode="before")
    @classmethod
    def _ensure_path(cls, value: Any) -> Path:
        if isinstance(value, Path):
            return value
        return Path(str(value))

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, value: Any) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    def configure_directories(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.model_cache_dir.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.configure_directories()
    return settings


