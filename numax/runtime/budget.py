from __future__ import annotations

from dataclasses import dataclass


class BudgetExceededError(RuntimeError):
    pass


@dataclass
class BudgetCharge:
    tokens: int = 0
    cost_usd: float = 0.0


def charge_budget(state, charge: BudgetCharge) -> None:
    state.budget.tokens_used += charge.tokens
    state.budget.cost_used_usd += charge.cost_usd

    state.add_trace(
        "budget",
        "post",
        "Budget charged",
        tokens_added=charge.tokens,
        cost_added_usd=charge.cost_usd,
        tokens_used=state.budget.tokens_used,
        cost_used_usd=state.budget.cost_used_usd,
    )

    if (
        state.budget.max_tokens_total is not None
        and state.budget.tokens_used > state.budget.max_tokens_total
    ):
        state.runtime.degraded = True
        state.runtime.fsm_state = "DEGRADED"
        raise BudgetExceededError("Token budget exceeded.")

    if (
        state.budget.max_cost_usd is not None
        and state.budget.cost_used_usd > state.budget.max_cost_usd
    ):
        state.runtime.degraded = True
        state.runtime.fsm_state = "DEGRADED"
        raise BudgetExceededError("Cost budget exceeded.")


def within_budget(state) -> bool:
    tokens_ok = (
        state.budget.max_tokens_total is None
        or state.budget.tokens_used <= state.budget.max_tokens_total
    )
    cost_ok = (
        state.budget.max_cost_usd is None or state.budget.cost_used_usd <= state.budget.max_cost_usd
    )
    return tokens_ok and cost_ok
