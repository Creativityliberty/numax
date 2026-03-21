from __future__ import annotations

from typing import Any

from numax.core.state import NumaxState
from numax.critic.confidence import aggregate_confidence


def build_session_diagnostics(state: NumaxState) -> dict[str, Any]:
    return {
        "run_id": state.runtime.run_id,
        "flow_name": state.runtime.flow_name,
        "fsm_state": state.runtime.fsm_state,
        "degraded": state.runtime.degraded,
        "budget": state.budget.model_dump(),
        "confidence": state.confidence.model_dump(),
        "aggregate_confidence": aggregate_confidence(state),
        "has_plan": state.plan is not None,
        "has_candidate_output": state.candidate_output is not None,
        "has_final_output": state.final_output is not None,
        "critique": state.critique.model_dump() if state.critique else None,
        "trace_count": len(state.trace),
    }
