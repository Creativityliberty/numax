from __future__ import annotations

import os

from numax.providers.base import (
    BaseProvider,
    CompletionRequest,
    CompletionResponse,
    ProviderHealth,
)


class AnthropicProvider(BaseProvider):
    provider_name = "anthropic"

    def __init__(self) -> None:
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self._models = ["claude-3-5-sonnet-latest", "claude-3-5-haiku-latest"]

    def list_models(self) -> list[str]:
        return self._models

    def health(self) -> ProviderHealth:
        if not self.api_key:
            return ProviderHealth(
                provider=self.provider_name, ok=False, notes=["Missing ANTHROPIC_API_KEY"]
            )
        return ProviderHealth(provider=self.provider_name, ok=True)

    def complete(self, model: str, request: CompletionRequest) -> CompletionResponse:
        return CompletionResponse(
            provider=self.provider_name,
            model=model,
            content=f"[Anthropic Stub] Response for {model}",
            usage={},
            raw={},
        )
