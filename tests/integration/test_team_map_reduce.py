from numax.core.state import NumaxState
from numax.flows.team_map_reduce import run_team_map_reduce


def test_team_map_reduce():
    base_state = NumaxState()

    result = run_team_map_reduce(
        base_state=base_state,
        missions=[
            {"team_id": "product_squad", "raw_input": "Mission A"},
            {"team_id": "engineering_squad", "raw_input": "Mission B"},
        ],
    )

    assert result["mission_count"] == 2
    assert len(result["results"]) == 2
