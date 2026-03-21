from numax.core.state import NumaxState
from numax.flows.specification_loop import build_specification_loop_flow


def test_specification_loop_flow():
    state = NumaxState(
        observation={"raw_input": "Fix the bug in the failing NUMAX repo test"}
    )

    graph = build_specification_loop_flow()
    final_state = graph.run(start="intent_spec", state=state)

    assert final_state.intent_spec
    assert final_state.work_spec
    assert final_state.spec_status in {"validated", "needs_clarification"}
