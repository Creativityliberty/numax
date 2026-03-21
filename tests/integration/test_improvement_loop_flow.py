from numax.core.state import NumaxState
from numax.flows.improvement_loop import build_improvement_loop_flow


def test_improvement_loop_flow_runs():
    state = NumaxState()
    state.last_test_run = {"ok": False}
    state.last_failure = {"kind": "test_failure"}

    graph = build_improvement_loop_flow()
    final_state = graph.run(start="improvement_loop", state=state)

    assert final_state.improvement_suggestions
    assert final_state.retry_decision
    assert final_state.improvement_status in {"retry_ready", "replan_ready", "stabilized"}
