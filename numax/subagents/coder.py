from __future__ import annotations

from typing import Any, Dict

from numax.core.state import NumaxState
from numax.subagents.base import BaseSubagent


class CoderSubagent(BaseSubagent):
    name = "coder_subagent"
    role = "coder"

    def act(self, state: NumaxState) -> Dict[str, Any]:
        notes = []
        suggested_action = "inspect_files"

        if state.active_files:
            notes.append(f"{len(state.active_files)} active files available.")
            suggested_action = "read_target_files"

        if state.last_patch:
            notes.append("Existing patch proposal found.")
            suggested_action = "refine_patch"

            apply_result = state.last_patch.get("apply_result", {})
            if apply_result.get("ok") and apply_result.get("preview_only", True):
                suggested_action = "apply_patch_real"
                notes.append("Patch preview succeeded; real apply may be considered.")

        if state.last_failure:
            suggested_action = "repair_after_failure"
            notes.append("A previous failure is recorded; prioritize repair.")

        return {
            "subagent": self.name,
            "role": self.role,
            "suggested_action": suggested_action,
            "notes": notes,
            "target_files": state.active_files,
            "patch": state.last_patch,
        }
