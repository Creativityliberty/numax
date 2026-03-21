from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class CompletionRequest(BaseModel):
    prompt: str
    system_prompt: str | None = None
    temperature: float = 0.2
    max_tokens: int | None = None
    response_format: str | None = None  # "text" | "json"


class CompletionResponse(BaseModel):
    provider: str
    model: str
    content: str
    usage: dict[str, Any] = Field(default_factory=dict)
    raw: dict[str, Any] = Field(default_factory=dict)


class ProviderHealth(BaseModel):
    provider: str
    ok: bool = True
    notes: list[str] = Field(default_factory=list)


class BaseProvider(ABC):
    provider_name: str = "base"

    @abstractmethod
    def list_models(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def health(self) -> ProviderHealth:
        raise NotImplementedError

    @abstractmethod
    def complete(self, model: str, request: CompletionRequest) -> CompletionResponse:
        raise NotImplementedError
