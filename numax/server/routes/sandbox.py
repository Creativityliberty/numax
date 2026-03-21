from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from numax.guardian.enforcer import enforce_sandbox_command

router = APIRouter()


class SandboxExecRequest(BaseModel):
    command: list[str] = Field(default_factory=list)
    cwd: str | None = None
    timeout_seconds: int = 10


@router.post("/exec")
def sandbox_exec(request: Request, payload: SandboxExecRequest) -> dict:
    auth = getattr(request.state, "auth", {}) or {}
    roles = auth.get("roles", [])
    return enforce_sandbox_command(
        user_roles=roles,
        command=payload.command,
        cwd=payload.cwd,
        timeout_seconds=payload.timeout_seconds,
    )
