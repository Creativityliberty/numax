from numax.core.state import NumaxState
from numax.flows.profile_apply import build_profile_apply_flow


def test_profile_apply_flow_runs():
    state = NumaxState(
        observation={
            "profile_id": "safe_demo_mode",
            "profile_preview": True,
        }
    )

    graph = build_profile_apply_flow()
    final_state = graph.run(start="profile_apply", state=state)

    assert final_state.profile_apply_result
