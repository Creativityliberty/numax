from __future__ import annotations

from typing import Any, Dict, Literal

from pydantic import BaseModel, Field


EventKind = Literal[
    "trace",
    "provider",
    "tool",
    "critic",
    "budget",
    "job",
    "sandbox",
    "unknown",
]


class RuntimeEvent(BaseModel):
    kind: EventKind = "unknown"
    name: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    severity: str = "info"  # info | warning | error
