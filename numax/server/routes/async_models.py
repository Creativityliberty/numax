from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.responses import StreamingResponse

from numax.providers.async_bootstrap import build_async_provider_registry
from numax.providers.base import CompletionRequest
from numax.reason.async_answer import AsyncAnswerEngine

router = APIRouter()


class AsyncCompleteRequest(BaseModel):
    provider: str | None = None
    model: str | None = None
    prompt: str
    retrieved_context: list[dict] = Field(default_factory=list)


@router.get("/providers")
async def list_async_providers() -> dict:
    registry = build_async_provider_registry()
    return {"providers": registry.list_providers()}


@router.post("/complete")
async def async_complete(request: AsyncCompleteRequest) -> dict:
    if request.provider and request.model:
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

    engine = AsyncAnswerEngine()
    return await engine.run(
        user_input=request.prompt,
        retrieved_context=request.retrieved_context,
        role="primary",
    )


@router.post("/stream")
async def async_stream(request: AsyncCompleteRequest) -> StreamingResponse:
    registry = build_async_provider_registry()
    provider_name = request.provider or "mock"
    model_name = request.model or "mock-large"
    provider = registry.get(provider_name)

    async def event_stream():
        async for chunk in provider.astream_complete(
            model_name,
            CompletionRequest(prompt=request.prompt, response_format="text"),
        ):
            yield chunk

    return StreamingResponse(event_stream(), media_type="text/plain")
