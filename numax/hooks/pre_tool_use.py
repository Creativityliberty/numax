from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from numax.guardian.permission_judge import judge_tool_permission
from numax.sandbox.manager import SandboxManager
from numax.tools.registry import ToolSpec


@dataclass
class PreToolUseDecision:
    action: str  # allow | deny | ask
    reason: str
    metadata: Dict[str, Any]


def pre_tool_use(
    tool_spec: ToolSpec,
    autonomy_mode: str,
    sandbox: SandboxManager,
) -> PreToolUseDecision:
    permission = judge_tool_permission(tool_spec, autonomy_mode=autonomy_mode)

    if permission.action == "deny":
        return PreToolUseDecision(
            action="deny",
            reason=permission.reason,
            metadata={"stage": "permission"},
        )

    if permission.action == "ask":
        return PreToolUseDecision(
            action="ask",
            reason=permission.reason,
            metadata={"stage": "permission"},
        )

    sandbox_check = sandbox.check_tool_execution(tool_spec.name)
    if not sandbox_check.allowed:
        return PreToolUseDecision(
            action="deny",
            reason=sandbox_check.reason,
            metadata={"stage": "sandbox", **sandbox_check.metadata},
        )

    return PreToolUseDecision(
        action="allow",
        reason="Tool allowed by permission and sandbox policy.",
        metadata={"stage": "ok", "sandbox_mode": sandbox.policy.mode},
    )
