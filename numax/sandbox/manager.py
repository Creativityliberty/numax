from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SandboxPolicy:
    mode: str = "none"  # none | read_only | isolated
    allow_file_write: bool = False
    allow_shell: bool = False
    allow_network: bool = False


@dataclass
class SandboxResult:
    allowed: bool
    reason: str
    metadata: dict[str, Any]


class SandboxManager:
    def __init__(self, policy: SandboxPolicy | None = None) -> None:
        self.policy = policy or SandboxPolicy()

    def check_tool_execution(self, tool_name: str) -> SandboxResult:
        if self.policy.mode == "none":
            return SandboxResult(
                allowed=True,
                reason="No sandbox restrictions enabled.",
                metadata={"mode": self.policy.mode},
            )

        if tool_name in {"echo", "summarize"}:
            return SandboxResult(
                allowed=True,
                reason="Low-risk tool allowed in sandbox.",
                metadata={"mode": self.policy.mode},
            )

        if self.policy.mode == "read_only":
            return SandboxResult(
                allowed=False,
                reason="Tool not allowed in read-only sandbox.",
                metadata={"mode": self.policy.mode},
            )

        if self.policy.mode == "isolated":
            return SandboxResult(
                allowed=False,
                reason="Tool requires explicit isolated implementation.",
                metadata={"mode": self.policy.mode},
            )

        return SandboxResult(
            allowed=False,
            reason="Unknown sandbox mode.",
            metadata={"mode": self.policy.mode},
        )
