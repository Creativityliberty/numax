from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.guardian.enforcer import enforce_external_subagent
from numax.subagents.orchestrator import SubagentOrchestrator


class ExternalSubagentNode(NumaxNode):
    name = "external_subagent"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "subagent_id": state.observation.get("external_subagent_id", "mock_repo_worker"),
            "mode": state.observation.get("external_subagent_mode", "read_only"),
            "user_roles": state.observation.get("user_roles", ["admin"]),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        guard = enforce_external_subagent(
            user_roles=payload["user_roles"],
            subagent_id=payload["subagent_id"],
            mode=payload["mode"],
        )
        return {"guard": guard}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        guard = result["guard"]

        if not guard["ok"]:
            state.external_subagent_result = guard
            state.next_recommended_action = "inspect_external_subagent_denial"
            state.add_trace(self.name, "post", "External subagent denied", guard=guard)
            return "done"

        orchestrator = SubagentOrchestrator()
        external_result = orchestrator.run_with_external(
            state=state,
            subagent_id=payload["subagent_id"],
            mode=payload["mode"],
        )

        state.external_subagent_result = external_result
        state.external_subagent_history.append(external_result)
        state.next_recommended_action = "review_external_subagent_result"

        state.add_trace(
            self.name,
            "post",
            "External subagent invoked",
            subagent_id=payload["subagent_id"],
            mode=payload["mode"],
        )
        return "done"
