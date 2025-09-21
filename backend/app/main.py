from __future__ import annotations

import asyncio
import sys

# Windows compatibility: ensure asyncio subprocesses work on Windows
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.schemas.voice import HealthResponse

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
)

cors_origins = settings.cors_origins
allow_any_origin = "*" in cors_origins
allow_origins = ["*"] if allow_any_origin else cors_origins
allow_credentials = not allow_any_origin

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

generated_dir = settings.storage_dir / "generated"
generated_dir.mkdir(parents=True, exist_ok=True)

app.include_router(
    api_router,
    prefix=f"{settings.api_prefix}/{settings.api_version}",
)

app.mount(
    f"{settings.api_prefix}/{settings.api_version}/files",
    StaticFiles(directory=generated_dir),
    name="generated-files",
)


@app.get("/")
def root() -> dict[str, object]:
    return {"ok": True, "message": "Voice Cloning API is running"}


@app.get(
    f"{settings.api_prefix}/health",
    response_model=HealthResponse,
)
def health() -> HealthResponse:
    return HealthResponse(environment=settings.environment)

