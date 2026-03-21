from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.improve.loop import run_improvement_loop


class ImprovementLoopNode(NumaxNode):
    name = "improvement_loop"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        snapshot = {
            "last_test_run": state.last_test_run,
            "code_review": state.world_state.get("code_review", {}),
            "spec_validation": state.world_state.get("spec_validation", {}),
            "last_failure": state.last_failure,
            "next_recommended_action": state.next_recommended_action,
            "runtime": {
                "retries": state.runtime.retries,
                "degraded": state.runtime.degraded,
                "max_retries": state.runtime.max_retries,
            },
            "confidence": {
                "safety_confidence": state.confidence.safety_confidence,
            },
        }
        return {"snapshot": snapshot}

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"improvement": run_improvement_loop(payload["snapshot"])}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        improvement = result["improvement"]

        state.improvement_suggestions = improvement["suggestions"]
        state.retry_decision = improvement["retry_decision"]
        state.mutation_decision = improvement["mutation_decision"]
        state.improvement_status = improvement["status"]

        retry_decision = improvement["retry_decision"]["decision"]
        if retry_decision == "retry":
            state.next_recommended_action = "retry_execution"
        elif retry_decision == "replan":
            state.next_recommended_action = "replan_execution"
        else:
            state.next_recommended_action = "stop_execution"

        state.add_trace(
            self.name,
            "post",
            "Improvement loop evaluated",
            status=improvement["status"],
            retry_decision=improvement["retry_decision"],
            mutation_decision=improvement["mutation_decision"],
        )
        return "done"
