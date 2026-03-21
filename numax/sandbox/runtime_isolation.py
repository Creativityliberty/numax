from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from numax.sandbox.policy import ALLOWED_COMMANDS, BLOCKED_TOKENS
from numax.sandbox.specs import SandboxCommand


class SandboxViolation(RuntimeError):
    pass


def run_isolated_command(spec: SandboxCommand) -> dict[str, Any]:
    if not spec.command:
        raise SandboxViolation("Empty command")

    exe = spec.command[0]
    if exe not in ALLOWED_COMMANDS:
        raise SandboxViolation(f"Command not allowed: {exe}")

    for token in spec.command:
        if token in BLOCKED_TOKENS:
            raise SandboxViolation(f"Blocked token: {token}")

    cwd = spec.cwd or "."
    cwd_path = Path(cwd).resolve()

    result = subprocess.run(
        spec.command,
        cwd=str(cwd_path),
        capture_output=True,
        text=True,
        timeout=spec.timeout_seconds,
        check=False,
    )

    return {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "command": spec.command,
        "cwd": str(cwd_path),
    }
