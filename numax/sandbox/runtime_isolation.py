from __future__ import annotations

from typing import Any, Dict

from numax.sandbox.container_runner import run_in_container
from numax.sandbox.fs_policy import is_path_allowed
from numax.sandbox.policy import ALLOWED_COMMANDS, BLOCKED_TOKENS
from numax.sandbox.specs import SandboxCommand


class SandboxViolation(RuntimeError):
    pass


def run_isolated_command(spec: SandboxCommand) -> Dict[str, Any]:
    if not spec.command:
        raise SandboxViolation("Empty command")

    exe = spec.command[0]
    if exe not in ALLOWED_COMMANDS:
        raise SandboxViolation(f"Command not allowed: {exe}")

    for token in spec.command:
        if token in BLOCKED_TOKENS:
            raise SandboxViolation(f"Blocked token: {token}")

    cwd = spec.cwd or "."
    if not is_path_allowed(cwd, ["."]):
        raise SandboxViolation(f"Path not allowed: {cwd}")

    return run_in_container(spec.command, cwd=cwd, timeout_seconds=spec.timeout_seconds)
