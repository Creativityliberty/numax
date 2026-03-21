from __future__ import annotations

from dataclasses import dataclass

from numax.critic.confidence import aggregate_confidence


@dataclass
class KillSwitchDecision:
    stop: bool
    degrade: bool
    escalate: bool
    reason: str
    violated_rules: list[str]


def evaluate_kill_switch(state) -> KillSwitchDecision:
    violated_rules: list[str] = []

    if state.confidence.safety_confidence < 0.6:
        violated_rules.append("safety_first")
        state.runtime.degraded = True
        state.runtime.fsm_state = "DEGRADED"
        return KillSwitchDecision(
            stop=True,
            degrade=True,
            escalate=False,
            reason="Safety confidence below threshold.",
            violated_rules=violated_rules,
        )

    if state.runtime.fsm_state == "HALT":
        violated_rules.append("governance_integrity")
        return KillSwitchDecision(
            stop=True,
            degrade=False,
            escalate=False,
            reason="Runtime FSM already in HALT.",
            violated_rules=violated_rules,
        )

    if (
        state.budget.max_cost_usd is not None
        and state.budget.cost_used_usd > state.budget.max_cost_usd
    ):
        violated_rules.append("control_cost")
        state.runtime.degraded = True
        state.runtime.fsm_state = "DEGRADED"
        return KillSwitchDecision(
            stop=True,
            degrade=True,
            escalate=False,
            reason="Cost budget exceeded.",
            violated_rules=violated_rules,
        )

    if (
        state.budget.max_tokens_total is not None
        and state.budget.tokens_used > state.budget.max_tokens_total
    ):
        violated_rules.append("control_cost")
        state.runtime.degraded = True
        state.runtime.fsm_state = "DEGRADED"
        return KillSwitchDecision(
            stop=True,
            degrade=True,
            escalate=False,
            reason="Token budget exceeded.",
            violated_rules=violated_rules,
        )

    if state.runtime.degraded and state.final_output is None:
        violated_rules.append("preserve_output_quality")
        return KillSwitchDecision(
            stop=True,
            degrade=True,
            escalate=True,
            reason="System is degraded and no valid output is available.",
            violated_rules=violated_rules,
        )

    if aggregate_confidence(state) < 0.2 and state.final_output is None:
        violated_rules.append("preserve_output_quality")
        return KillSwitchDecision(
            stop=True,
            degrade=False,
            escalate=True,
            reason="Confidence collapsed before final output.",
            violated_rules=violated_rules,
        )

    return KillSwitchDecision(
        stop=False,
        degrade=False,
        escalate=False,
        reason="No kill-switch condition met.",
        violated_rules=[],
    )
