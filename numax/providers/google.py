from __future__ import annotations

import os

import httpx

from numax.providers.base import (
    BaseProvider,
    CompletionRequest,
    CompletionResponse,
    ProviderHealth,
)


class GoogleProvider(BaseProvider):
    provider_name = "google"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")

    def list_models(self) -> list[str]:
        return [
            "gemini-3.1-pro-preview",
            "gemini-3-flash-preview",
            "gemini-2.5-pro",
            "gemini-2.5-flash",
        ]

    def health(self) -> ProviderHealth:
        if not self.api_key:
            return ProviderHealth(
                provider=self.provider_name,
                ok=False,
                notes=["GOOGLE_API_KEY not found in environment"],
            )
        return ProviderHealth(provider=self.provider_name, ok=True)

    def complete(self, model: str, request: CompletionRequest) -> CompletionResponse:
        if not self.api_key:
            raise RuntimeError("GOOGLE_API_KEY not set")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"

        payload = {
            "contents": [{"parts": [{"text": request.prompt}]}],
            "generationConfig": {
                "temperature": request.temperature,
            },
        }

        if request.max_tokens:
            payload["generationConfig"]["maxOutputTokens"] = request.max_tokens

        if request.response_format == "json":
            payload["generationConfig"]["responseMimeType"] = "application/json"

        if request.system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": request.system_prompt}]}

        with httpx.Client() as client:
            resp = client.post(url, json=payload, timeout=60.0)
            resp.raise_for_status()

            data = resp.json()

            try:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                content = ""

            usage = data.get("usageMetadata", {})

            return CompletionResponse(
                provider=self.provider_name,
                model=model,
                content=content,
                usage={
                    "input_tokens": usage.get("promptTokenCount", 0),
                    "output_tokens": usage.get("candidatesTokenCount", 0),
                },
                raw=data,
            )
