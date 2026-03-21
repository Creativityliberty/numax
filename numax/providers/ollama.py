from __future__ import annotations

import os

import httpx

from numax.providers.base import (
    BaseProvider,
    CompletionRequest,
    CompletionResponse,
    ProviderHealth,
)


class OllamaProvider(BaseProvider):
    provider_name = "ollama"

    def __init__(self) -> None:
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self._models = ["llama3.1", "qwen2.5"]

    def list_models(self) -> list[str]:
        return self._models

    def health(self) -> ProviderHealth:
        try:
            with httpx.Client(timeout=5.0) as client:
                r = client.get(f"{self.base_url}/api/tags")
                r.raise_for_status()
            return ProviderHealth(provider=self.provider_name, ok=True)
        except Exception as exc:
            return ProviderHealth(provider=self.provider_name, ok=False, notes=[str(exc)])

    def complete(self, model: str, request: CompletionRequest) -> CompletionResponse:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": request.prompt,
            "stream": False,
        }

        with httpx.Client(timeout=60.0) as client:
            r = client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()

        content = data.get("response", "")
        usage = {
            "input_tokens": data.get("prompt_eval_count", 0),
            "output_tokens": data.get("eval_count", 0),
        }
        return CompletionResponse(
            provider=self.provider_name,
            model=model,
            content=content,
            usage=usage,
            raw=data,
        )
