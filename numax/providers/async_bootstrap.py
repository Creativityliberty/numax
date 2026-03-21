from __future__ import annotations

from numax.configs.loader import get_provider_config, load_config
from numax.providers.async_mock import AsyncMockProvider
from numax.providers.async_openai import AsyncOpenAIProvider
from numax.providers.async_registry import AsyncProviderRegistry


def build_async_provider_registry() -> AsyncProviderRegistry:
    registry = AsyncProviderRegistry()
    config = load_config()
    provider_cfg = get_provider_config(config)

    if provider_cfg.get("mock", {}).get("enabled", True):
        registry.register(AsyncMockProvider())

    if provider_cfg.get("openai", {}).get("enabled", False):
        registry.register(AsyncOpenAIProvider())

    return registry
