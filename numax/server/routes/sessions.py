from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

SESSIONS_DIR = Path("data/state/sessions")
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


class CreateSessionRequest(BaseModel):
    goal: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


def _session_path(session_id: str) -> Path:
    return SESSIONS_DIR / f"{session_id}.json"


@router.post("/")
def create_session(request: CreateSessionRequest) -> dict:
    session_id = str(uuid.uuid4())
    payload = {
        "session_id": session_id,
        "goal": request.goal,
        "metadata": request.metadata,
        "status": "created",
    }

    _session_path(session_id).write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    return payload


@router.get("/")
def list_sessions() -> list[dict]:
    rows = []
    for file in SESSIONS_DIR.glob("*.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            rows.append(data)
        except Exception:
            continue
    return rows


@router.get("/{session_id}")
def get_session(session_id: str) -> dict:
    path = _session_path(session_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Session not found")
    return json.loads(path.read_text(encoding="utf-8"))


@router.get("/{session_id}/diagnostics")
def get_session_diagnostics(session_id: str) -> dict:
    path = _session_path(session_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Session not found")

    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        "session_id": payload["session_id"],
        "status": payload.get("status"),
        "goal": payload.get("goal", {}),
        "metadata": payload.get("metadata", {}),
        "notes": ["Session diagnostics are minimal in v0.1"],
    }
