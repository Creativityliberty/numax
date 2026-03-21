from numax.core.state import NumaxState


def test_state_starts_empty_and_valid():
    state = NumaxState()

    assert state.goal == {}
    assert state.observation == {}
    assert state.runtime.fsm_state == "IDLE"
    assert state.budget.tokens_used == 0
    assert state.trace == []


def test_add_trace_appends_event():
    state = NumaxState()

    state.add_trace("test_node", "prep", "Preparing")

    assert len(state.trace) == 1
    assert state.trace[0].node == "test_node"
    assert state.trace[0].phase == "prep"
    assert state.trace[0].message == "Preparing"
