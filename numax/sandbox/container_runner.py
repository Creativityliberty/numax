from __future__ import annotations

from typing import Any, Dict, List


def run_in_container(command: list[str], cwd: str | None = None, timeout_seconds: int = 20) -> Dict[str, Any]:
    return {
        "ok": True,
        "mode": "container_stub",
        "command": command,
        "cwd": cwd,
        "timeout_seconds": timeout_seconds,
        "stdout": "container execution stub",
        "stderr": "",
        "returncode": 0,
    }
