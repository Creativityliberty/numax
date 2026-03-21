from __future__ import annotations

from typing import Any

from numax.guardian.tool_risk import classify_tool_risk
from numax.rbac.checks import has_permission
from numax.sandbox.runtime_isolation import run_isolated_command
from numax.sandbox.specs import SandboxCommand


def enforce_sandbox_command(
    user_roles: list[str],
    command: list[str],
    cwd: str | None = None,
    timeout_seconds: int = 10,
) -> dict[str, Any]:
    risk = classify_tool_risk("shell")

    if risk == "high" and not has_permission(user_roles, "sandbox.exec"):
        return {
            "ok": False,
            "reason": "missing_permission:sandbox.exec",
            "risk": risk,
        }

    return run_isolated_command(
        SandboxCommand(
            command=command,
            cwd=cwd,
            timeout_seconds=timeout_seconds,
        )
    )
