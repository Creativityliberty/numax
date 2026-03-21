from __future__ import annotations

from numax.providers.async_base import AsyncBaseProvider


class AsyncProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, AsyncBaseProvider] = {}

    def register(self, provider: AsyncBaseProvider) -> None:
        self._providers[provider.provider_name] = provider

    def get(self, provider_name: str) -> AsyncBaseProvider:
        if provider_name not in self._providers:
            raise KeyError(f"Unknown async provider: {provider_name}")
        return self._providers[provider_name]

    def list_providers(self) -> list[str]:
        return sorted(self._providers.keys())
