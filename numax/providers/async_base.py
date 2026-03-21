from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from numax.providers.base import CompletionRequest, CompletionResponse, ProviderHealth


class AsyncBaseProvider(ABC):
    provider_name: str = "unknown_async"

    @abstractmethod
    async def acomplete(self, model: str, request: CompletionRequest) -> CompletionResponse:
        raise NotImplementedError

    @abstractmethod
    async def ahealth(self) -> ProviderHealth:
        raise NotImplementedError

    @abstractmethod
    async def alist_models(self) -> list[str]:
        raise NotImplementedError

    async def astream_complete(
        self,
        model: str,
        request: CompletionRequest,
    ) -> AsyncIterator[str]:
        response = await self.acomplete(model, request)
        yield response.content
