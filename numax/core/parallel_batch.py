from __future__ import annotations

from typing import Any, Dict, List

from numax.core.parallel_flow import ParallelFlow
from numax.core.state import NumaxState


class ParallelBatch:
    def __init__(self, flow_builder, start: str, max_workers: int = 4) -> None:
        self.parallel_flow = ParallelFlow(
            flow_builder=flow_builder,
            start=start,
            name="parallel_batch",
            max_workers=max_workers,
        )

    def run(self, base_state: NumaxState, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return self.parallel_flow.run(base_state=base_state, parallel_inputs=items)
