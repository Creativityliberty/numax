from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CompletionRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.2
    max_tokens: Optional[int] = None
    response_format: Optional[str] = None  # "text" | "json"


class CompletionResponse(BaseModel):
    provider: str
    model: str
    content: str
    usage: Dict[str, Any] = Field(default_factory=dict)
    raw: Dict[str, Any] = Field(default_factory=dict)


class ProviderHealth(BaseModel):
    provider: str
    ok: bool = True
    notes: List[str] = Field(default_factory=list)


class BaseProvider(ABC):
    provider_name: str = "base"

    @abstractmethod
    def list_models(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def health(self) -> ProviderHealth:
        raise NotImplementedError

    @abstractmethod
    def complete(self, model: str, request: CompletionRequest) -> CompletionResponse:
        raise NotImplementedError
