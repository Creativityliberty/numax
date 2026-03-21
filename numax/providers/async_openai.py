from __future__ import annotations

import os
from collections.abc import AsyncIterator

import httpx

from numax.providers.async_base import AsyncBaseProvider
from numax.providers.base import CompletionRequest, CompletionResponse, ProviderHealth


class AsyncOpenAIProvider(AsyncBaseProvider):
    provider_name = "openai"

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self._models = ["gpt-4.1", "gpt-4.1-mini"]

    async def alist_models(self) -> list[str]:
        return self._models

    async def ahealth(self) -> ProviderHealth:
        if not self.api_key:
            return ProviderHealth(
                provider=self.provider_name,
                ok=False,
                notes=["Missing OPENAI_API_KEY"],
            )
        return ProviderHealth(provider=self.provider_name, ok=True)

    async def acomplete(self, model: str, request: CompletionRequest) -> CompletionResponse:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured.")

        url = f"{self.base_url}/responses"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "input": request.prompt,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()

        content = ""
        try:
            output = data.get("output", [])
            if output and output[0].get("content"):
                content = output[0]["content"][0].get("text", "")
        except Exception:
            content = str(data)

        usage = data.get("usage", {})
        return CompletionResponse(
            provider=self.provider_name,
            model=model,
            content=content,
            usage=usage,
            raw=data,
        )

    async def astream_complete(
        self,
        model: str,
        request: CompletionRequest,
    ) -> AsyncIterator[str]:
        response = await self.acomplete(model, request)
        text = response.content or ""
        chunk_size = 120
        for i in range(0, len(text), chunk_size):
            yield text[i : i + chunk_size]
