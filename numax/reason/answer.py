from __future__ import annotations

from typing import Any, Dict

from numax.bootstrap import (
    build_model_catalog,
    build_model_resolver,
    build_provider_registry,
)
from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.providers.base import CompletionRequest


class AnswerNode(NumaxNode):
    name = "answer"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        payload = {
            "user_input": state.observation.get("raw_input", ""),
            "retrieved_context": state.retrieved_context,
        }
        state.add_trace(self.name, "prep", "Answer payload prepared")
        return payload

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        registry = build_provider_registry()
        catalog = build_model_catalog()
        resolver = build_model_resolver(catalog)

        model_spec = resolver.resolve(role="primary")
        provider = registry.get(model_spec.provider)

        prompt = payload["user_input"]
        if payload["retrieved_context"]:
            prompt += f"\n\nContext: {payload['retrieved_context']}"

        response = provider.complete(
            model=model_spec.model_name,
            request=CompletionRequest(
                prompt=prompt,
                response_format="text",
            ),
        )

        return {
            "candidate_output": {
                "text": response.content,
                "provider": response.provider,
                "model": response.model,
                "usage": response.usage,
            }
        }

    def post(
        self,
        state: NumaxState,
        payload: Dict[str, Any],
        result: Dict[str, Any],
    ) -> str:
        state.candidate_output = result["candidate_output"]
        state.confidence.output_confidence = 0.75
        state.runtime.fsm_state = "DELIVER"
        return "critic"
