from __future__ import annotations

from typing import Any

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.guardian.permission_judge import judge_tool_permission
from numax.tools.default_tools import build_default_tool_registry


class ToolConfirmationRouterNode(NumaxNode):
    name = "tool_confirmation_router"

    def prep(self, state: NumaxState) -> dict[str, Any]:
        tool_request = state.world_state.get("tool_request")
        if not tool_request:
            raise ValueError("No tool_request found in world_state.")

        payload = {
            "tool_name": tool_request["tool_name"],
            "tool_args": tool_request.get("tool_args", {}),
            "autonomy_mode": state.world_state.get("autonomy_mode", "ASSISTED"),
        }
        state.add_trace(self.name, "prep", "Tool confirmation payload prepared", **payload)
        return payload

    def exec(self, payload: dict[str, Any]) -> dict[str, Any]:
        registry = build_default_tool_registry()
        tool = registry.get(payload["tool_name"])

        decision = judge_tool_permission(
            tool_spec=tool.spec,
            autonomy_mode=payload["autonomy_mode"],
        )

        return {
            "decision": decision.action,
            "reason": decision.reason,
        }

    def post(
        self,
        state: NumaxState,
        payload: dict[str, Any],
        result: dict[str, Any],
    ) -> str:
        state.world_state["tool_permission"] = result
        state.add_trace(
            self.name,
            "post",
            "Tool permission decision recorded",
            decision=result["decision"],
            reason=result["reason"],
        )

        if result["decision"] == "allow":
            return "allow"

        if result["decision"] == "ask":
            state.runtime.degraded = True
            state.runtime.fsm_state = "DEGRADED"
            return "ask"

        state.runtime.degraded = True
        state.runtime.fsm_state = "HALT"
        return "deny"
