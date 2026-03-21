from __future__ import annotations

from typing import Any, Dict

from numax.improve.mutation_gate import evaluate_mutation_gate
from numax.improve.retry_policy import decide_retry_policy
from numax.improve.suggester import suggest_improvements


def run_improvement_loop(state_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    suggestions_result = suggest_improvements(state_snapshot)
    suggestions = suggestions_result["suggestions"]

    retry_decision = decide_retry_policy(
        suggestions=suggestions,
        retries=state_snapshot.get("runtime", {}).get("retries", 0),
        max_retries=state_snapshot.get("runtime", {}).get("max_retries", 3),
    )

    mutation_decision = evaluate_mutation_gate(
        suggestions=suggestions,
        safety_confidence=state_snapshot.get("confidence", {}).get("safety_confidence", 1.0),
        degraded=state_snapshot.get("runtime", {}).get("degraded", False),
    )

    if retry_decision["decision"] == "stop":
        status = "stabilized"
    elif retry_decision["decision"] == "retry":
        status = "retry_ready"
    else:
        status = "replan_ready"

    return {
        "suggestions": suggestions,
        "retry_decision": retry_decision,
        "mutation_decision": mutation_decision,
        "status": status,
    }
