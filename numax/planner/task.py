from __future__ import annotations

from typing import Any

from numax.core.node import NumaxNode
from numax.core.state import NumaxState


class PlannerNode(NumaxNode):
    name = "planner"

    def prep(self, state: NumaxState) -> dict[str, Any]:
        payload = {
            "user_input": state.observation.get("raw_input", ""),
        }
        state.add_trace(self.name, "prep", "Planner payload prepared", **payload)
        return payload

    def exec(self, payload: dict[str, Any]) -> dict[str, Any]:
        user_input = str(payload["user_input"]).strip().lower()

        steps: list[dict[str, Any]] = []

        retrieval_keywords = [
            "search",
            "research",
            "document",
            "source",
            "file",
            "reference",
            "citation",
        ]

        if any(keyword in user_input for keyword in retrieval_keywords):
            steps.append(
                {
                    "id": "step_retrieve",
                    "objective": "Retrieve relevant context",
                    "node": "retrieve",
                    "status": "proposed",
                }
            )

        steps.append(
            {
                "id": "step_answer",
                "objective": "Produce candidate answer",
                "node": "answer",
                "status": "proposed",
            }
        )

        steps.append(
            {
                "id": "step_critic",
                "objective": "Validate candidate output",
                "node": "basic_critic",
                "status": "proposed",
            }
        )

        return {
            "plan": {
                "strategy": "linear_minimal_plan",
                "steps": steps,
            }
        }

    def post(
        self,
        state: NumaxState,
        payload: dict[str, Any],
        result: dict[str, Any],
    ) -> str:
        state.plan = result["plan"]
        state.runtime.fsm_state = "PLAN"
        state.add_trace(self.name, "post", "Plan created", plan=state.plan)

        step_nodes = [step["node"] for step in state.plan["steps"]]
        if "retrieve" in step_nodes:
            return "retrieve"

        return "answer"
