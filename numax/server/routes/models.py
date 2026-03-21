from __future__ import annotations

from fastapi import APIRouter

from numax.bootstrap import build_model_catalog

router = APIRouter()


@router.get("/")
def list_models() -> list[dict]:
    catalog = build_model_catalog()
    return [model.model_dump() for model in catalog.all()]


@router.get("/enabled")
def list_enabled_models() -> list[dict]:
    catalog = build_model_catalog()
    return [model.model_dump() for model in catalog.list_enabled()]


@router.get("/role/{role}")
def list_models_by_role(role: str) -> list[dict]:
    catalog = build_model_catalog()
    return [model.model_dump() for model in catalog.list_by_role(role)]


@router.get("/capability/{capability}")
def list_models_by_capability(capability: str) -> list[dict]:
    catalog = build_model_catalog()
    return [model.model_dump() for model in catalog.list_by_capability(capability)]
