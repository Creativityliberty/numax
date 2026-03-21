from __future__ import annotations

from typing import Any

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.tools.default_tools import build_default_tool_registry


class ToolNode(NumaxNode):
    name = "tool"

    def prep(self, state: NumaxState) -> dict[str, Any]:
        tool_request = state.world_state.get("tool_request")
        if not tool_request:
            raise ValueError("No tool_request found in world_state.")

        payload = {
            "tool_name": tool_request["tool_name"],
            "tool_args": tool_request.get("tool_args", {}),
        }
        state.add_trace(self.name, "prep", "Tool payload prepared", **payload)
        return payload

    def exec(self, payload: dict[str, Any]) -> dict[str, Any]:
        registry = build_default_tool_registry()
        result = registry.call(payload["tool_name"], **payload["tool_args"])
        return {"tool_result": result}

    def post(
        self,
        state: NumaxState,
        payload: dict[str, Any],
        result: dict[str, Any],
    ) -> str:
        state.world_state["tool_result"] = result["tool_result"]
        return "default"
