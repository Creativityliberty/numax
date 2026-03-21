from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.learning.router import route_intent_adaptive


class IntentRouterNode(NumaxNode):
    name = "intent_router"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        state.runtime.fsm_state = "UNDERSTAND"

        user_input = state.observation.get("raw_input", "")
        payload = {
            "user_input": user_input,
            "has_context": len(state.retrieved_context) > 0,
        }
        state.add_trace(self.name, "prep", "Intent router payload prepared", **payload)
        return payload

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return route_intent_adaptive(
            user_input=payload["user_input"],
            has_context=payload["has_context"],
        )

    def post(
        self,
        state: NumaxState,
        payload: Dict[str, Any],
        result: Dict[str, Any],
    ) -> str:
        route = result["route"]
        state.confidence.understanding_confidence = result["understanding_confidence"]
        state.world_state["intent_route"] = route
        state.world_state["routing_policy"] = result.get("routing_policy")

        if route == "retrieve":
            state.runtime.fsm_state = "PLAN"
            return "retrieve"

        state.runtime.fsm_state = "BUILD"
        return "answer"
