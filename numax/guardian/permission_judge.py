from __future__ import annotations

from dataclasses import dataclass

from numax.tools.registry import ToolSpec


@dataclass
class PermissionDecision:
    action: str  # allow | deny | ask
    reason: str


def judge_tool_permission(
    tool_spec: ToolSpec,
    autonomy_mode: str = "ASSISTED",
) -> PermissionDecision:
    """
    Minimal NUMAX v0.1 permission policy.
    """

    if tool_spec.risk_level == "low":
        return PermissionDecision(
            action="allow",
            reason="Low-risk tool.",
        )

    if tool_spec.risk_level == "medium":
        if tool_spec.requires_confirmation or autonomy_mode == "ASSISTED":
            return PermissionDecision(
                action="ask",
                reason="Medium-risk tool requires confirmation in current mode.",
            )
        return PermissionDecision(
            action="allow",
            reason="Medium-risk tool allowed in current autonomy mode.",
        )

    if tool_spec.risk_level == "high":
        if autonomy_mode in {"ASSISTED", "SEMI_AUTONOMOUS"}:
            return PermissionDecision(
                action="ask",
                reason="High-risk tool requires explicit confirmation.",
            )
        return PermissionDecision(
            action="deny",
            reason="High-risk tool denied in current autonomy mode.",
        )

    return PermissionDecision(
        action="deny",
        reason="Unknown risk level.",
    )
