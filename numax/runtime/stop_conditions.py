from __future__ import annotations

from dataclasses import dataclass

from numax.critic.confidence import aggregate_confidence


@dataclass
class StopDecision:
    should_stop: bool
    reason: str | None = None
    should_degrade: bool = False


def evaluate_stop_conditions(state) -> StopDecision:
    """
    Minimal NUMAX v0.1 stop policy.
    """

    if state.runtime.fsm_state == "HALT":
        return StopDecision(True, reason="FSM already in HALT")

    if state.runtime.degraded:
        return StopDecision(True, reason="Runtime already degraded", should_degrade=True)

    if state.confidence.safety_confidence < 0.6:
        state.runtime.degraded = True
        state.runtime.fsm_state = "DEGRADED"
        return StopDecision(
            True,
            reason="Safety confidence below threshold",
            should_degrade=True,
        )

    if (
        state.budget.max_tokens_total is not None
        and state.budget.tokens_used > state.budget.max_tokens_total
    ):
        state.runtime.degraded = True
        state.runtime.fsm_state = "DEGRADED"
        return StopDecision(
            True,
            reason="Token budget exceeded",
            should_degrade=True,
        )

    if (
        state.budget.max_cost_usd is not None
        and state.budget.cost_used_usd > state.budget.max_cost_usd
    ):
        state.runtime.degraded = True
        state.runtime.fsm_state = "DEGRADED"
        return StopDecision(
            True,
            reason="Cost budget exceeded",
            should_degrade=True,
        )

    global_conf = aggregate_confidence(state)
    if state.final_output is None and global_conf < 0.2:
        return StopDecision(
            True,
            reason="Confidence too low and no valid output available",
            should_degrade=False,
        )

    return StopDecision(False)
