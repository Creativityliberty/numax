from __future__ import annotations

from typing import Any, Dict, List

from numax.core.parallel_batch import ParallelBatch
from numax.core.state import NumaxState
from numax.flows.team_run import build_team_run_flow


def run_team_map_reduce(base_state: NumaxState, missions: List[Dict[str, Any]]) -> Dict[str, Any]:
    parallel = ParallelBatch(
        flow_builder=build_team_run_flow,
        start="team_load",
        max_workers=4,
    )

    mapped = parallel.run(base_state=base_state, items=missions)

    consolidated = {
        "mission_count": len(missions),
        "results": mapped,
        "teams": sorted(
            {
                item["observation"].get("team_id", "unknown")
                for item in mapped
            }
        ),
    }

    return consolidated
