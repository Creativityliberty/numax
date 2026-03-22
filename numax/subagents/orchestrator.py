from __future__ import annotations

from typing import Any, Dict

from numax.core.state import NumaxState
from numax.subagents.coder import CoderSubagent
from numax.subagents.contracts import ExternalSubagentRequest
from numax.subagents.external import build_default_external_subagent_registry
from numax.subagents.operator import OperatorSubagent
from numax.subagents.reviewer import ReviewerSubagent
from numax.learning.mode_selector import select_best_mode


class SubagentOrchestrator:
    def __init__(self) -> None:
        self.operator = OperatorSubagent()
        self.coder = CoderSubagent()
        self.reviewer = ReviewerSubagent()
        self.external_registry = build_default_external_subagent_registry()

    def recommend_best_config(self, group_by: str = "profile") -> Dict[str, Any]:
        return select_best_mode(group_by=group_by, min_runs=1)

    def run_all(self, state: NumaxState) -> Dict[str, Any]:
        operator_result = self.operator.act(state)
        coder_result = self.coder.act(state)
        reviewer_result = self.reviewer.act(state)

        return {
            "operator": operator_result,
            "coder": coder_result,
            "reviewer": reviewer_result,
        }

    def run_with_external(
        self,
        state: NumaxState,
        subagent_id: str,
        mode: str = "read_only",
    ) -> Dict[str, Any]:
        provider = self.external_registry.get(subagent_id)

        request = ExternalSubagentRequest(
            task=state.observation.get("raw_input", "No explicit task"),
            workspace_path=state.active_workspace.get("root_path"),
            active_files=state.active_files,
            context={
                "next_recommended_action": state.next_recommended_action,
                "test_command": state.observation.get("test_command", ["pytest", "-q"]),
            },
            mode=mode,
            max_steps=5,
        )

        response = provider.invoke(request)

        return {
            "external": response.model_dump(),
            "internal": self.run_all(state),
        }
