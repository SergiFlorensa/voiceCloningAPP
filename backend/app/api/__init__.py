from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.voice_clone import router as voice_clone_router

api_router = APIRouter()
api_router.include_router(voice_clone_router)

__all__ = ["api_router"]
