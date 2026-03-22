from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List

from numax.core.state import NumaxState


class ParallelFlow:
    def __init__(self, flow_builder, start: str, name: str = "parallel_flow", max_workers: int = 4) -> None:
        self.flow_builder = flow_builder
        self.start = start
        self.name = name
        self.max_workers = max_workers

    def _run_one(self, base_state: NumaxState, item: Dict[str, Any]) -> Dict[str, Any]:
        state = base_state.model_copy(deep=True)
        state.observation.update(item)

        graph = self.flow_builder()
        final_state = graph.run(start=self.start, state=state)

        return {
            "observation": item,
            "final_output": final_state.final_output,
            "team_results": final_state.team_results,
            "next_recommended_action": final_state.next_recommended_action,
        }

    def run(self, base_state: NumaxState, parallel_inputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self._run_one, base_state, item) for item in parallel_inputs]
            for future in as_completed(futures):
                results.append(future.result())

        return results
