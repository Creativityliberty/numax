from __future__ import annotations

from typing import Any, Dict

from numax.core.state import NumaxState
from numax.subagents.coder import CoderSubagent
from numax.subagents.operator import OperatorSubagent
from numax.subagents.reviewer import ReviewerSubagent


class SubagentOrchestrator:
    def __init__(self) -> None:
        self.operator = OperatorSubagent()
        self.coder = CoderSubagent()
        self.reviewer = ReviewerSubagent()

    def run_all(self, state: NumaxState) -> Dict[str, Any]:
        operator_result = self.operator.act(state)
        coder_result = self.coder.act(state)
        reviewer_result = self.reviewer.act(state)

        return {
            "operator": operator_result,
            "coder": coder_result,
            "reviewer": reviewer_result,
        }
