import pytest

from numax.core.state import NumaxState
from numax.runtime.budget import BudgetCharge, BudgetExceededError, charge_budget


def test_budget_charge_updates_state():
    state = NumaxState()
    state.budget.max_tokens_total = 100
    state.budget.max_cost_usd = 10.0

    charge_budget(state, BudgetCharge(tokens=15, cost_usd=0.25))

    assert state.budget.tokens_used == 15
    assert state.budget.cost_used_usd == 0.25


def test_budget_exceeded_raises():
    state = NumaxState()
    state.budget.max_tokens_total = 10

    with pytest.raises(BudgetExceededError):
        charge_budget(state, BudgetCharge(tokens=11, cost_usd=0.0))

    assert state.runtime.degraded is True
    assert state.runtime.fsm_state == "DEGRADED"
