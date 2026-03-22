from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class BlackboardEntry(BaseModel):
    entry_id: str
    team_id: str
    artifact_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class BlackboardState(BaseModel):
    entries: List[BlackboardEntry] = Field(default_factory=list)


def add_blackboard_entry(state: BlackboardState, entry: BlackboardEntry) -> BlackboardState:
    state.entries.append(entry)
    return state


def list_blackboard_entries(state: BlackboardState, artifact_type: str | None = None) -> list[dict]:
    out = []
    for entry in state.entries:
        if artifact_type and entry.artifact_type != artifact_type:
            continue
        out.append(entry.model_dump())
    return out
