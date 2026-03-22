from numax.core.batch_flow import BatchFlow
from numax.core.state import NumaxState
from numax.flows.team_run import build_team_run_flow


def test_batch_flow_runs():
    flow = BatchFlow(build_team_run_flow, start="team_load")
    base_state = NumaxState()

    results = flow.run(
        base_state=base_state,
        batch_inputs=[
            {"team_id": "product_squad", "raw_input": "Prepare spec"},
            {"team_id": "qa_squad", "raw_input": "Review output"},
        ],
    )

    assert len(results) == 2
