from numax.core.state import NumaxState
from numax.flows.blackboard_cycle import build_blackboard_cycle_flow


def test_blackboard_cycle_flow():
    state = NumaxState(
        observation={
            "team_id": "product_squad",
            "artifact_type": "spec",
            "artifact_payload": {"objective": "Implement NUMAX V3"},
            "consume_team_id": "engineering_squad",
        }
    )

    graph = build_blackboard_cycle_flow()
    final_state = graph.run(start="blackboard_publish", state=state)

    assert final_state.blackboard_state["entries"]
    assert "engineering_squad" in final_state.subscription_state
