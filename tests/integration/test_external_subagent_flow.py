from numax.core.state import NumaxState
from numax.flows.external_subagent_run import build_external_subagent_run_flow


def test_external_subagent_run_flow_runs():
    state = NumaxState(
        observation={
            "raw_input": "Inspect the repo",
            "external_subagent_id": "mock_repo_worker",
            "external_subagent_mode": "read_only",
            "user_roles": ["admin"],
        }
    )

    graph = build_external_subagent_run_flow()
    final_state = graph.run(start="external_subagent", state=state)

    assert final_state.external_subagent_result
