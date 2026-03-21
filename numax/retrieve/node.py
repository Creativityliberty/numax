from __future__ import annotations

from typing import Any

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.retrieve.engine import SimpleRetrievalEngine

DEFAULT_DOCUMENTS = [
    {
        "id": "numax_intro",
        "text": "NUMAX is a governed agentic cortex designed "
        "to transform intent into structured artifacts.",
    },
    {
        "id": "numax_memory",
        "text": "NUMAX includes working memory, episodic memory, "
        "semantic memory and continuity mechanisms.",
    },
    {
        "id": "numax_runtime",
        "text": "NUMAX uses runtime policies, model routing, "
        "budget guards and fallback strategies.",
    },
]


class RetrieveNode(NumaxNode):
    name = "retrieve"

    def prep(self, state: NumaxState) -> dict[str, Any]:
        payload = {
            "query": state.observation.get("raw_input", ""),
        }
        state.add_trace(self.name, "prep", "Retrieve payload prepared", **payload)
        return payload

    def exec(self, payload: dict[str, Any]) -> dict[str, Any]:
        engine = SimpleRetrievalEngine(DEFAULT_DOCUMENTS)
        results = engine.search(query=payload["query"], top_k=3)
        return {
            "results": [
                {
                    "source_id": item.source_id,
                    "text": item.text,
                    "score": item.score,
                }
                for item in results
            ]
        }

    def post(
        self,
        state: NumaxState,
        payload: dict[str, Any],
        result: dict[str, Any],
    ) -> str:
        state.retrieved_context = result["results"]

        if state.retrieved_context:
            state.confidence.source_confidence = min(
                1.0,
                max(item["score"] for item in state.retrieved_context) / 3.0,
            )
        else:
            state.confidence.source_confidence = 0.0

        state.runtime.fsm_state = "BUILD"
        return "answer"
