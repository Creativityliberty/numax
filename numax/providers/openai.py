from __future__ import annotations

import os

from numax.providers.base import (
    BaseProvider,
    CompletionRequest,
    CompletionResponse,
    ProviderHealth,
)


class OpenAIProvider(BaseProvider):
    provider_name = "openai"

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self._models = ["gpt-4.1", "gpt-4.1-mini"]

    def list_models(self) -> list[str]:
        return self._models

    def health(self) -> ProviderHealth:
        if not self.api_key:
            return ProviderHealth(
                provider=self.provider_name, ok=False, notes=["Missing OPENAI_API_KEY"]
            )
        return ProviderHealth(provider=self.provider_name, ok=True)

    def complete(self, model: str, request: CompletionRequest) -> CompletionResponse:
        return CompletionResponse(
            provider=self.provider_name,
            model=model,
            content=f"[OpenAI Stub] Response for {model}",
            usage={},
            raw={},
        )
