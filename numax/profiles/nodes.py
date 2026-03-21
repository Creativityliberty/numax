from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.profiles.apply import apply_profile


class ProfileApplyNode(NumaxNode):
    name = "profile_apply"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "profile_id": state.observation.get("profile_id", ""),
            "preview": state.observation.get("profile_preview", True),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        result = apply_profile(
            profile_id=payload["profile_id"],
            preview=payload["preview"],
        )
        return {
            "profile_apply_result": {
                "ok": result.ok,
                "profile_id": result.profile_id,
                "notes": result.notes,
            }
        }

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        apply_result = result["profile_apply_result"]
        state.profile_apply_result = apply_result

        if apply_result["ok"]:
            state.active_profile = apply_result["profile_id"]
            state.profile_history.append(apply_result["profile_id"])

        state.next_recommended_action = (
            "run_profile_target_flow" if apply_result["ok"] else "inspect_profile_failure"
        )

        state.add_trace(
            self.name,
            "post",
            "Profile application completed",
            result=apply_result,
        )
        return "done"
