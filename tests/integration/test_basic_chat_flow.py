from numax.core.state import NumaxState
from numax.flows.basic_chat import build_basic_chat_flow


def test_basic_chat_flow_produces_output():
    graph = build_basic_chat_flow()
    state = NumaxState(observation={"raw_input": "Explain NUMAX simply"})
    state.runtime.run_id = "test-basic-chat"

    final_state = graph.run(start="intent_router", state=state)

    assert final_state.final_output is not None
    assert final_state.critique is not None
    assert final_state.critique.ok is True
