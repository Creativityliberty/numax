from __future__ import annotations

from numax.core.batch_flow import BatchFlow
from numax.core.state import NumaxState
from numax.flows.team_run import build_team_run_flow


def run_team_batch(base_state: NumaxState, batch_inputs: list[dict]) -> list[dict]:
    flow = BatchFlow(
        flow_builder=build_team_run_flow,
        start="team_load",
        name="team_batch_run",
    )
    return flow.run(base_state=base_state, batch_inputs=batch_inputs)
