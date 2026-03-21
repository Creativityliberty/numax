from __future__ import annotations

from numax.providers.base import (
    BaseProvider,
    CompletionRequest,
    CompletionResponse,
    ProviderHealth,
)


class MockProvider(BaseProvider):
    provider_name = "mock"

    def __init__(self) -> None:
        self._models = ["mock-small", "mock-large"]

    def list_models(self) -> list[str]:
        return self._models

    def health(self) -> ProviderHealth:
        return ProviderHealth(provider=self.provider_name, ok=True)

    def complete(self, model: str, request: CompletionRequest) -> CompletionResponse:
        return CompletionResponse(
            provider=self.provider_name,
            model=model,
            content=f"[{model}] mock completion for: {request.prompt}",
            usage={
                "input_tokens": len(request.prompt.split()),
                "output_tokens": 8,
            },
            raw={},
        )
