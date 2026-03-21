from numax.core.state import NumaxState
from numax.flows.subagent_review import build_subagent_review_flow


def test_subagent_review_flow_runs():
    state = NumaxState()
    graph = build_subagent_review_flow()
    final_state = graph.run(start="subagent_orchestrate", state=state)

    assert final_state.subagent_plan
    assert final_state.active_subagent == "operator_subagent"
