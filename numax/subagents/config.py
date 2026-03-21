from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

PermissionMode = Literal[
    "default",
    "acceptEdits",
    "bypassPermissions",
    "plan",
]

ReturnMode = Literal[
    "final_only",
    "with_trace",
    "structured",
]


class SubagentConfig(BaseModel):
    name: str
    description: str = ""
    max_turns: int = 4
    timeout_seconds: int = 60
    allowed_tools: list[str] = Field(default_factory=list)
    disallowed_tools: list[str] = Field(default_factory=list)
    permission_mode: PermissionMode = "default"
    return_mode: ReturnMode = "final_only"
    sandbox_mode: str = "read_only"
    fallback_model_role: str | None = None
