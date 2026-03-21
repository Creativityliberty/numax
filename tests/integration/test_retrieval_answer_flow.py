from numax.core.state import NumaxState
from numax.flows.retrieval_answer import build_retrieval_answer_flow


def test_retrieval_answer_flow_uses_context():
    graph = build_retrieval_answer_flow()
    state = NumaxState(observation={"raw_input": "What are the memory mechanisms of NUMAX?"})
    state.runtime.run_id = "test-retrieval"

    final_state = graph.run(start="intent_router", state=state)

    assert final_state.final_output is not None
    assert final_state.retrieved_context is not None
    assert len(final_state.trace) > 0
