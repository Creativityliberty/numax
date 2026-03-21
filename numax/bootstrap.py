from __future__ import annotations

from numax.configs.loader import load_config, get_provider_config, get_routing_config
from numax.models.catalog import ModelCatalog, ModelSpec
from numax.models.resolver import ModelResolver, RuntimePolicy
from numax.providers.anthropic import AnthropicProvider
from numax.providers.google import GoogleProvider
from numax.providers.mock import MockProvider
from numax.providers.ollama import OllamaProvider
from numax.providers.openai import OpenAIProvider
from numax.providers.registry import ProviderRegistry


def build_provider_registry() -> ProviderRegistry:
    registry = ProviderRegistry()
    config = load_config()
    provider_cfg = get_provider_config(config)

    if provider_cfg.get("mock", {}).get("enabled", True):
        registry.register(MockProvider())

    if provider_cfg.get("openai", {}).get("enabled", False):
        registry.register(OpenAIProvider())

    if provider_cfg.get("anthropic", {}).get("enabled", False):
        registry.register(AnthropicProvider())

    if provider_cfg.get("google", {}).get("enabled", False):
        registry.register(GoogleProvider())

    if provider_cfg.get("ollama", {}).get("enabled", False):
        registry.register(OllamaProvider())

    return registry


def build_model_catalog() -> ModelCatalog:
    catalog = ModelCatalog()

    catalog.register(
        ModelSpec(
            id="mock:mock-small",
            provider="mock",
            model_name="mock-small",
            roles=["light"],
            capabilities=["chat"],
            supports_json=False,
            supports_tools=False,
        )
    )
    catalog.register(
        ModelSpec(
            id="mock:mock-large",
            provider="mock",
            model_name="mock-large",
            roles=["primary", "critic"],
            capabilities=["chat", "json"],
            supports_json=True,
            supports_tools=False,
        )
    )

    catalog.register(
        ModelSpec(
            id="openai:gpt-4.1",
            provider="openai",
            model_name="gpt-4.1",
            roles=["primary", "critic"],
            capabilities=["chat", "json", "tools"],
            supports_json=True,
            supports_tools=True,
        )
    )
    catalog.register(
        ModelSpec(
            id="openai:gpt-4.1-mini",
            provider="openai",
            model_name="gpt-4.1-mini",
            roles=["light"],
            capabilities=["chat", "json", "tools"],
            supports_json=True,
            supports_tools=True,
        )
    )

    catalog.register(
        ModelSpec(
            id="anthropic:claude-3-5-sonnet-latest",
            provider="anthropic",
            model_name="claude-3-5-sonnet-latest",
            roles=["primary", "critic"],
            capabilities=["chat", "json"],
            supports_json=True,
        )
    )
    catalog.register(
        ModelSpec(
            id="anthropic:claude-3-5-haiku-latest",
            provider="anthropic",
            model_name="claude-3-5-haiku-latest",
            roles=["light"],
            capabilities=["chat", "json"],
            supports_json=True,
        )
    )

    catalog.register(
        ModelSpec(
            id="google:gemini-1.5-pro",
            provider="google",
            model_name="gemini-1.5-pro",
            roles=["primary", "critic"],
            capabilities=["chat", "json"],
            supports_json=True,
        )
    )
    catalog.register(
        ModelSpec(
            id="google:gemini-1.5-flash",
            provider="google",
            model_name="gemini-1.5-flash",
            roles=["light"],
            capabilities=["chat", "json"],
            supports_json=True,
        )
    )

    catalog.register(
        ModelSpec(
            id="ollama:llama3.1",
            provider="ollama",
            model_name="llama3.1",
            roles=["primary"],
            capabilities=["chat"],
            supports_json=False,
        )
    )
    catalog.register(
        ModelSpec(
            id="ollama:qwen2.5",
            provider="ollama",
            model_name="qwen2.5",
            roles=["light"],
            capabilities=["chat"],
            supports_json=False,
        )
    )

    return catalog


def build_model_resolver(catalog: ModelCatalog) -> ModelResolver:
    config = load_config()
    routing_cfg = get_routing_config(config)

    preferred = {
        "primary": routing_cfg.get("primary", "mock:mock-large"),
        "light": routing_cfg.get("light", "mock:mock-small"),
        "critic": routing_cfg.get("critic", "mock:mock-large"),
    }

    raw_fallbacks = routing_cfg.get("fallbacks", {})
    fallbacks = {
        "primary": raw_fallbacks.get("primary", ["mock:mock-small"]),
        "critic": raw_fallbacks.get("critic", ["mock:mock-small"]),
        "light": raw_fallbacks.get("light", []),
    }

    policy = RuntimePolicy(preferred=preferred, fallbacks=fallbacks)
    return ModelResolver(catalog=catalog, policy=policy)
