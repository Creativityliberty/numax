from __future__ import annotations

from numax.tools.registry import Tool, ToolRegistry, ToolSpec


def echo_tool(text: str) -> dict:
    return {"echo": text}


def summarize_tool(text: str) -> dict:
    short = text[:120]
    return {"summary": short}


def build_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        Tool(
            spec=ToolSpec(
                name="echo",
                description="Return the provided text as-is.",
                risk_level="low",
                requires_confirmation=False,
                tags=["utility"],
            ),
            handler=echo_tool,
        )
    )

    registry.register(
        Tool(
            spec=ToolSpec(
                name="summarize",
                description="Return a short summary of the provided text.",
                risk_level="low",
                requires_confirmation=False,
                tags=["text", "utility"],
            ),
            handler=summarize_tool,
        )
    )

    return registry
