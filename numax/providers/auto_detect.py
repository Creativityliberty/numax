from __future__ import annotations

import os
from typing import Any

from numax.providers.anthropic import AnthropicProvider
from numax.providers.google import GoogleProvider
from numax.providers.ollama import OllamaProvider
from numax.providers.openai import OpenAIProvider


def detect_enabled_providers() -> list[str]:
    enabled: list[str] = []

    if os.getenv("OPENAI_API_KEY"):
        enabled.append("openai")
    if os.getenv("ANTHROPIC_API_KEY"):
        enabled.append("anthropic")
    if os.getenv("GOOGLE_API_KEY"):
        enabled.append("google")
    if os.getenv("OLLAMA_BASE_URL"):
        enabled.append("ollama")

    return enabled


def build_auto_providers() -> list:
    providers: list[Any] = []
    names = detect_enabled_providers()

    if "openai" in names:
        providers.append(OpenAIProvider())
    if "anthropic" in names:
        providers.append(AnthropicProvider())
    if "google" in names:
        providers.append(GoogleProvider())
    if "ollama" in names:
        providers.append(OllamaProvider())

    return providers
