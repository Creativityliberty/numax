from numax.core.parallel_flow import ParallelFlow
from numax.core.state import NumaxState
from numax.flows.team_run import build_team_run_flow


def test_parallel_flow_runs():
    flow = ParallelFlow(build_team_run_flow, start="team_load", max_workers=2)
    base_state = NumaxState()

    results = flow.run(
        base_state=base_state,
        parallel_inputs=[
            {"team_id": "product_squad", "raw_input": "Prepare spec"},
            {"team_id": "engineering_squad", "raw_input": "Implement patch"},
        ],
    )

    assert len(results) == 2
