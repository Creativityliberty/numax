from __future__ import annotations

from typing import Any, Dict, List

from numax.core.state import NumaxState


class BatchFlow:
    def __init__(self, flow_builder, start: str, name: str = "batch_flow") -> None:
        self.flow_builder = flow_builder
        self.start = start
        self.name = name

    def run(self, base_state: NumaxState, batch_inputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        for item in batch_inputs:
            state = base_state.model_copy(deep=True)
            state.observation.update(item)

            graph = self.flow_builder()
            final_state = graph.run(start=self.start, state=state)

            results.append(
                {
                    "observation": item,
                    "final_output": final_state.final_output,
                    "team_results": final_state.team_results,
                    "next_recommended_action": final_state.next_recommended_action,
                }
            )

        return results
