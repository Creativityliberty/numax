from __future__ import annotations

from fastapi import APIRouter

from numax.bootstrap import build_provider_registry

router = APIRouter()


@router.get("/")
def list_providers() -> list[str]:
    registry = build_provider_registry()
    return registry.list_providers()


@router.get("/models")
def list_provider_models() -> list[dict]:
    registry = build_provider_registry()
    return registry.list_models()


@router.get("/health")
def provider_health() -> list[dict]:
    registry = build_provider_registry()
    return [item.model_dump() for item in registry.health()]
