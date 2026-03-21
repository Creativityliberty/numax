from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from numax.providers.async_bootstrap import build_async_provider_registry
from numax.providers.base import CompletionRequest

router = APIRouter()


class AsyncCompleteRequest(BaseModel):
    provider: str
    model: str
    prompt: str


@router.get("/providers")
async def list_async_providers() -> dict:
    registry = build_async_provider_registry()
    return {"providers": registry.list_providers()}


@router.post("/complete")
async def async_complete(request: AsyncCompleteRequest) -> dict:
    registry = build_async_provider_registry()
    provider = registry.get(request.provider)
    response = await provider.acomplete(
        request.model,
        CompletionRequest(prompt=request.prompt, response_format="text"),
    )
    return {
        "provider": response.provider,
        "model": response.model,
        "content": response.content,
        "usage": response.usage,
    }


@router.post("/stream")
async def async_stream(request: AsyncCompleteRequest) -> StreamingResponse:
    registry = build_async_provider_registry()
    provider = registry.get(request.provider)

    async def event_stream():
        async for chunk in provider.astream_complete(
            request.model,
            CompletionRequest(prompt=request.prompt, response_format="text"),
        ):
            yield chunk

    return StreamingResponse(event_stream(), media_type="text/plain")
