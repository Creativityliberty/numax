from __future__ import annotations

from typing import Any, Dict

from numax.core.state import NumaxState
from numax.subagents.base import BaseSubagent


class OperatorSubagent(BaseSubagent):
    name = "operator_subagent"
    role = "operator"

    def act(self, state: NumaxState) -> Dict[str, Any]:
        notes = []

        if not state.active_workspace:
            decision = "open_workspace"
            notes.append("No active workspace found.")
        elif not state.world_state.get("workspace_search"):
            decision = "search_code"
            notes.append("Workspace is open but no code search has been performed yet.")
        elif not state.last_patch:
            decision = "propose_patch"
            notes.append("Search results exist but no patch proposal is available.")
        elif not state.last_test_run:
            decision = "run_tests"
            notes.append("A patch exists but no test run has been recorded.")
        elif state.world_state.get("code_review"):
            review = state.world_state["code_review"]
            decision = review.get("decision", "revise")
            notes.append(f"Code review decision is '{decision}'.")
        else:
            decision = state.next_recommended_action or "inspect_state"
            notes.append("Falling back to next recommended action from runtime state.")

        return {
            "subagent": self.name,
            "role": self.role,
            "decision": decision,
            "notes": notes,
        }
