from __future__ import annotations

from typing import Any

from numax.core.node import NumaxNode
from numax.core.state import NumaxState


class IntentRouterNode(NumaxNode):
    name = "intent_router"

    def prep(self, state: NumaxState) -> dict[str, Any]:
        state.runtime.fsm_state = "UNDERSTAND"

        user_input = state.observation.get("raw_input", "")
        retrieved_context = state.retrieved_context
        source_conf = state.confidence.source_confidence

        payload = {
            "user_input": user_input,
            "has_context": len(retrieved_context) > 0,
            "source_confidence": source_conf,
        }
        state.add_trace(self.name, "prep", "Intent router payload prepared", **payload)
        return payload

    def exec(self, payload: dict[str, Any]) -> dict[str, Any]:
        text = str(payload["user_input"]).strip().lower()

        needs_retrieval_keywords = [
            "source",
            "document",
            "file",
            "reference",
            "citation",
            "research",
            "search",
            "look up",
        ]

        if any(keyword in text for keyword in needs_retrieval_keywords):
            return {
                "route": "retrieve",
                "understanding_confidence": 0.85,
            }

        if payload["has_context"] and payload["source_confidence"] >= 0.5:
            return {
                "route": "answer",
                "understanding_confidence": 0.80,
            }

        return {
            "route": "answer",
            "understanding_confidence": 0.70,
        }

    def post(
        self,
        state: NumaxState,
        payload: dict[str, Any],
        result: dict[str, Any],
    ) -> str:
        route = result["route"]
        state.confidence.understanding_confidence = result["understanding_confidence"]
        state.world_state["intent_route"] = route

        if route == "retrieve":
            state.runtime.fsm_state = "PLAN"
            return "retrieve"

        state.runtime.fsm_state = "BUILD"
        return "answer"
