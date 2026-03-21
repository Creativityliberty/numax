from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Dict, List


def run_tests(
    root_path: str,
    command: list[str] | None = None,
    timeout_seconds: int = 120,
) -> Dict[str, Any]:
    root = Path(root_path).resolve()
    cmd = command or ["pytest", "-q"]

    try:
        result = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        return {
            "ok": result.returncode == 0,
            "root_path": str(root),
            "command": cmd,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "root_path": str(root),
            "command": cmd,
        }
