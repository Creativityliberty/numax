from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from numax.storage.bootstrap import build_default_store
from numax.storage.repos import SessionRepository

router = APIRouter()
repo = SessionRepository(build_default_store())


class CreateSessionRequest(BaseModel):
    goal: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


@router.post("/")
def create_session(request: CreateSessionRequest) -> dict:
    session_id = str(uuid.uuid4())
    payload = {
        "session_id": session_id,
        "goal": request.goal,
        "metadata": request.metadata,
        "status": "created",
    }
    repo.save(session_id, payload)
    return payload


@router.get("/")
def list_sessions() -> list[dict]:
    keys = [k for k in repo.store.list_keys() if k.startswith("sessions/")]
    rows = []
    for k in keys:
        try:
            val = repo.store.get(k)
            if val:
                rows.append(val)
        except Exception:
            continue
    return rows


@router.get("/{session_id}")
def get_session(session_id: str) -> dict:
    data = repo.get(session_id)
    if not data:
        raise HTTPException(status_code=404, detail="Session not found")
    return data


@router.get("/{session_id}/diagnostics")
def get_session_diagnostics(session_id: str) -> dict:
    payload = repo.get(session_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": payload["session_id"],
        "status": payload.get("status"),
        "goal": payload.get("goal", {}),
        "metadata": payload.get("metadata", {}),
        "notes": ["Session diagnostics are minimal in v0.1"],
    }
