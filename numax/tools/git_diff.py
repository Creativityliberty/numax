from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Dict


def get_git_diff(root_path: str, staged: bool = False) -> Dict[str, Any]:
    root = Path(root_path).resolve()

    cmd = ["git", "diff"]
    if staged:
        cmd.append("--staged")

    try:
        result = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        return {
            "ok": result.returncode == 0,
            "root_path": str(root),
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "staged": staged,
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "root_path": str(root),
            "staged": staged,
        }
