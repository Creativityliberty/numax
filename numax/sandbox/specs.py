from __future__ import annotations

from pydantic import BaseModel, Field


class SandboxCommand(BaseModel):
    command: list[str] = Field(default_factory=list)
    cwd: str | None = None
    timeout_seconds: int = 10
