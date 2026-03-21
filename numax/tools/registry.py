from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolSpec:
    name: str
    description: str
    risk_level: str = "low"  # low | medium | high
    requires_confirmation: bool = False
    tags: list[str] = field(default_factory=list)


@dataclass
class Tool:
    spec: ToolSpec
    handler: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.spec.name in self._tools:
            raise ValueError(f"Tool '{tool.spec.name}' already registered.")
        self._tools[tool.spec.name] = tool

    def get(self, tool_name: str) -> Tool:
        if tool_name not in self._tools:
            raise KeyError(f"Unknown tool: {tool_name}")
        return self._tools[tool_name]

    def list_tools(self) -> list[ToolSpec]:
        return [tool.spec for tool in self._tools.values()]

    def call(self, tool_name: str, **kwargs: Any) -> Any:
        tool = self.get(tool_name)
        return tool.handler(**kwargs)
