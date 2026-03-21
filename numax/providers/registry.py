from __future__ import annotations

from numax.providers.base import BaseProvider, ProviderHealth


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, BaseProvider] = {}

    def register(self, provider: BaseProvider) -> None:
        name = provider.provider_name
        if name in self._providers:
            raise ValueError(f"Provider '{name}' already registered.")
        self._providers[name] = provider

    def get(self, provider_name: str) -> BaseProvider:
        if provider_name not in self._providers:
            raise KeyError(f"Unknown provider: {provider_name}")
        return self._providers[provider_name]

    def list_providers(self) -> list[str]:
        return sorted(self._providers.keys())

    def list_models(self) -> list[dict]:
        rows: list[dict] = []
        for provider_name, provider in self._providers.items():
            for model in provider.list_models():
                rows.append(
                    {
                        "provider": provider_name,
                        "model": model,
                        "id": f"{provider_name}:{model}",
                    }
                )
        return rows

    def health(self) -> list[ProviderHealth]:
        return [provider.health() for provider in self._providers.values()]
