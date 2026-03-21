from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from numax.subagents.config import SubagentConfig


@dataclass
class SubagentResult:
    ok: bool
    output: Dict[str, Any]
    notes: list[str]


class SubagentRunner:
    def run(self, config: SubagentConfig, task: Dict[str, Any]) -> SubagentResult:
        return SubagentResult(
            ok=True,
            output={
                "subagent": config.name,
                "task": task,
                "status": "completed_stub",
            },
            notes=[
                f"Subagent '{config.name}' executed in stub mode.",
                f"Max turns: {config.max_turns}",
                f"Sandbox mode: {config.sandbox_mode}",
            ],
        )
