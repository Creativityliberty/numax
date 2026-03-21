from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.subagents.orchestrator import SubagentOrchestrator


class SubagentOrchestrateNode(NumaxNode):
    name = "subagent_orchestrate"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {}

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Return empty dict as the actual orchestration logic is currently in post() 
        # as per user's implementation snippet, but I'll move it here for better practice.
        # Wait, I'll follow user's snippet to be safe.
        return {}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        orchestrator = SubagentOrchestrator()
        subagent_result = orchestrator.run_all(state)

        state.subagent_plan = subagent_result
        state.active_subagent = "operator_subagent"
        state.subagent_notes = (
            subagent_result["operator"].get("notes", [])
            + subagent_result["coder"].get("notes", [])
            + subagent_result["reviewer"].get("notes", [])
        )

        operator_decision = subagent_result["operator"].get("decision")
        state.next_recommended_action = operator_decision

        state.add_trace(
            self.name,
            "post",
            "Subagent orchestration completed",
            operator=subagent_result["operator"],
            coder=subagent_result["coder"],
            reviewer=subagent_result["reviewer"],
        )
        return "done"
