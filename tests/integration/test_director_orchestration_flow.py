from numax.core.state import NumaxState
from numax.flows.director_orchestration import build_director_orchestration_flow


def test_director_orchestration_flow():
    state = NumaxState(
        observation={
            "raw_input": "Build NUMAX V3 AI Factory",
        }
    )

    graph = build_director_orchestration_flow()
    final_state = graph.run(start="director_plan", state=state)

    assert final_state.director_plan
    assert final_state.director_results
