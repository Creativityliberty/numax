from __future__ import annotations

from collections.abc import AsyncIterator

from numax.providers.async_base import AsyncBaseProvider
from numax.providers.base import CompletionRequest, CompletionResponse, ProviderHealth


class AsyncMockProvider(AsyncBaseProvider):
    provider_name = "mock"

    async def alist_models(self) -> list[str]:
        return ["mock-small", "mock-large"]

    async def ahealth(self) -> ProviderHealth:
        return ProviderHealth(provider=self.provider_name, ok=True)

    async def acomplete(self, model: str, request: CompletionRequest) -> CompletionResponse:
        content = f"[async-mock:{model}] {request.prompt}"
        usage = {"input_tokens": len(request.prompt.split()), "output_tokens": len(content.split())}
        return CompletionResponse(
            provider=self.provider_name,
            model=model,
            content=content,
            usage=usage,
            raw={"mock": True},
        )

    async def astream_complete(
        self,
        model: str,
        request: CompletionRequest,
    ) -> AsyncIterator[str]:
        content = f"[async-mock:{model}] {request.prompt}"
        for token in content.split():
            yield token + " "
