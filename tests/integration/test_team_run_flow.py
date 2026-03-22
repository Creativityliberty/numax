from numax.core.state import NumaxState
from numax.flows.team_run import build_team_run_flow


def test_team_run_flow():
    state = NumaxState(
        observation={
            "team_id": "product_squad",
            "raw_input": "Prepare product specification for NUMAX V3",
        }
    )

    graph = build_team_run_flow()
    final_state = graph.run(start="team_load", state=state)

    assert final_state.team_results
    assert "product_squad" in final_state.team_results
