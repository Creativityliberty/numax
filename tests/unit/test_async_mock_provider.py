import asyncio

from numax.providers.async_mock import AsyncMockProvider
from numax.providers.base import CompletionRequest


async def _run():
    provider = AsyncMockProvider()
    response = await provider.acomplete("mock-large", CompletionRequest(prompt="hello"))
    return response


def test_async_mock_provider_completes() -> None:
    response = asyncio.run(_run())
    assert response.provider == "mock"
    assert response.content
