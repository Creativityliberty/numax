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


def enforce_external_subagent(
    user_roles: list[str],
    subagent_id: str,
    mode: str,
) -> dict[str, Any]:
    if not has_permission(user_roles, "providers.use"):
        return {
            "ok": False,
            "reason": "missing_permission:providers.use",
            "subagent_id": subagent_id,
        }

    if mode in {"patch_proposal", "test_execution", "full_bounded"} and not has_permission(
        user_roles, "jobs.run"
    ):
        return {
            "ok": False,
            "reason": "missing_permission:jobs.run",
            "subagent_id": subagent_id,
        }

    return {
        "ok": True,
        "subagent_id": subagent_id,
        "mode": mode,
    }
