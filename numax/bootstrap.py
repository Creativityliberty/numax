from __future__ import annotations

import os

from numax.models.catalog import ModelCatalog, ModelSpec
from numax.models.resolver import ModelResolver, RuntimePolicy
from numax.providers.mock import MockProvider
from numax.providers.google import GoogleProvider
from numax.providers.registry import ProviderRegistry


def build_provider_registry() -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(MockProvider())
    registry.register(GoogleProvider())
    return registry


def build_model_catalog() -> ModelCatalog:
    catalog = ModelCatalog()

    # Mock models
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

    # Google Gemini Models (from docs/1.md)
    catalog.register(
        ModelSpec(
            id="google:gemini-3.1-pro-preview",
            provider="google",
            model_name="gemini-3.1-pro-preview",
            roles=["primary", "critic"],
            capabilities=["chat", "json", "vision"],
            supports_json=True,
            supports_tools=True,
            pricing={"input": 2.0, "output": 12.0}
        )
    )

    catalog.register(
        ModelSpec(
            id="google:gemini-3-flash-preview",
            provider="google",
            model_name="gemini-3-flash-preview",
            roles=["primary", "light", "critic"],
            capabilities=["chat", "json", "vision"],
            supports_json=True,
            supports_tools=True,
            pricing={"input": 0.5, "output": 3.0}
        )
    )
    
    catalog.register(
        ModelSpec(
            id="google:gemini-2.5-flash",
            provider="google",
            model_name="gemini-2.5-flash",
            roles=["light"],
            capabilities=["chat", "json", "vision"],
            supports_json=True,
            supports_tools=True,
            pricing={"input": 0.3, "output": 2.5}
        )
    )

    return catalog


def build_model_resolver(catalog: ModelCatalog) -> ModelResolver:
    # Check if google key is available to decide preferred models
    has_google = bool(os.getenv("GOOGLE_API_KEY"))

    if has_google:
        preferred = {
            "primary": "google:gemini-3.1-pro-preview",
            "light": "google:gemini-3-flash-preview",
            "critic": "google:gemini-3-flash-preview",
        }
        fallbacks = {
            "primary": ["google:gemini-2.5-flash"],
            "critic": ["google:gemini-2.5-flash"],
        }
    else:
        preferred = {
            "primary": "mock:mock-large",
            "light": "mock:mock-small",
            "critic": "mock:mock-large",
        }
        fallbacks = {
            "primary": ["mock:mock-small"],
            "critic": ["mock:mock-small"],
        }

    policy = RuntimePolicy(
        preferred=preferred,
        fallbacks=fallbacks,
    )
    return ModelResolver(catalog=catalog, policy=policy)
