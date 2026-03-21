from __future__ import annotations

from numax.tools.registry import Tool, ToolRegistry, ToolSpec
from numax.tools.workspace_tools import WorkspaceTools


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

    ws = WorkspaceTools()

    registry.register(
        Tool(
            spec=ToolSpec(
                name="workspace.read_file",
                description="Read a file from the active workspace",
                risk_level="low",
                requires_confirmation=False,
                tags=["workspace", "file", "read"],
            ),
            handler=ws.read,
        )
    )

    registry.register(
        Tool(
            spec=ToolSpec(
                name="workspace.write_file",
                description="Write a file in the active workspace",
                risk_level="high",
                requires_confirmation=True,
                tags=["workspace", "file", "write"],
            ),
            handler=ws.write,
        )
    )

    registry.register(
        Tool(
            spec=ToolSpec(
                name="workspace.search_code",
                description="Search code/text in the active workspace",
                risk_level="low",
                requires_confirmation=False,
                tags=["workspace", "search", "code"],
            ),
            handler=ws.search,
        )
    )

    registry.register(
        Tool(
            spec=ToolSpec(
                name="workspace.git_diff",
                description="Read git diff from the active workspace",
                risk_level="low",
                requires_confirmation=False,
                tags=["workspace", "git", "diff"],
            ),
            handler=ws.diff,
        )
    )

    registry.register(
        Tool(
            spec=ToolSpec(
                name="workspace.run_tests",
                description="Run tests in the active workspace",
                risk_level="high",
                requires_confirmation=True,
                tags=["workspace", "tests", "exec"],
            ),
            handler=ws.test,
        )
    )

    return registry
