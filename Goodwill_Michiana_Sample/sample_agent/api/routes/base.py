"""Base routes."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root() -> dict:
    return {"service": "goodwill-michiana-copilot-agent", "status": "ok"}


@router.get("/health")
async def health() -> dict:
    return {"status": "healthy"}
