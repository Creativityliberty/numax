from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List

from numax.subagents.contracts import ExternalSubagentRequest, ExternalSubagentResponse


class ExternalSubagentProvider(ABC):
    subagent_id: str = "unknown"
    description: str = ""

    @abstractmethod
    def invoke(self, request: ExternalSubagentRequest) -> ExternalSubagentResponse:
        raise NotImplementedError


class ExternalSubagentRegistry:
    def __init__(self) -> None:
        self._providers: Dict[str, ExternalSubagentProvider] = {}

    def register(self, provider: ExternalSubagentProvider) -> None:
        self._providers[provider.subagent_id] = provider

    def get(self, subagent_id: str) -> ExternalSubagentProvider:
        if subagent_id not in self._providers:
            raise KeyError(f"Unknown external subagent: {subagent_id}")
        return self._providers[subagent_id]

    def list_ids(self) -> list[str]:
        return sorted(self._providers.keys())
