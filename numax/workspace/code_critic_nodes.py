from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.critic.code_critic import review_code_change


class WorkspaceCodeCriticNode(NumaxNode):
    name = "workspace_code_critic"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "patch": state.last_patch,
            "test_result": state.last_test_run,
            "active_files": state.active_files,
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        review = review_code_change(
            patch=payload["patch"],
            test_result=payload["test_result"],
            active_files=payload["active_files"],
        )
        return {"review": review}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        review = result["review"]
        state.world_state["code_review"] = review
        state.patch_risk = review["risk"]
        state.change_scope = review["scope"]

        decision = review["decision"]
        if decision == "accept":
            state.next_recommended_action = "finalize_change"
        elif decision == "revise":
            state.next_recommended_action = "revise_patch"
        else:
            state.next_recommended_action = "revert_patch"

        state.add_trace(
            self.name,
            "post",
            "Code critic review completed",
            decision=decision,
            confidence=review["confidence"],
            risk=review["risk"],
            scope=review["scope"],
        )
        return "done"
