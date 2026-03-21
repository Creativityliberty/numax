from numax.core.state import NumaxState
from numax.flows.learning_feedback import build_learning_feedback_flow


def test_learning_feedback_flow_runs():
    state = NumaxState(
        observation={
            "task_type": "repair",
            "mode_candidates": ["repo_operator", "research_mode"],
        }
    )
    state.runtime.run_id = "run-test-learning"
    state.active_profile = "repo_operator"

    graph = build_learning_feedback_flow()
    final_state = graph.run(start="learning_feedback", state=state)

    assert final_state.active_feedback
    assert final_state.mode_recommendation
    assert final_state.learning_history
