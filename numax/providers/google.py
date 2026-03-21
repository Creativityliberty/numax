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

    def __init__(self) -> None:
        self.api_key = os.getenv("GOOGLE_API_KEY", "")
        self.base_url = os.getenv(
            "GOOGLE_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"
        )
        self._models = ["gemini-1.5-pro", "gemini-1.5-flash"]

    def list_models(self) -> list[str]:
        return self._models

    def health(self) -> ProviderHealth:
        if not self.api_key:
            return ProviderHealth(
                provider=self.provider_name, ok=False, notes=["Missing GOOGLE_API_KEY"]
            )
        return ProviderHealth(provider=self.provider_name, ok=True)

    def complete(self, model: str, request: CompletionRequest) -> CompletionResponse:
        if not self.api_key:
            raise RuntimeError("GOOGLE_API_KEY is not configured.")

        url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": request.prompt}],
                }
            ]
        }

        with httpx.Client(timeout=30.0) as client:
            r = client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()

        content = ""
        try:
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                content = "".join(part.get("text", "") for part in parts)
        except Exception:
            content = str(data)

        usage = data.get("usageMetadata", {})
        return CompletionResponse(
            provider=self.provider_name,
            model=model,
            content=content,
            usage=usage,
            raw=data,
        )
