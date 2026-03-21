from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def read_file(path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    target = Path(path).resolve()

    if not target.exists():
        return {
            "ok": False,
            "error": "file_not_found",
            "path": str(target),
        }

    if not target.is_file():
        return {
            "ok": False,
            "error": "not_a_file",
            "path": str(target),
        }

    try:
        content = target.read_text(encoding=encoding)
        return {
            "ok": True,
            "path": str(target),
            "content": content,
            "size_bytes": target.stat().st_size,
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "path": str(target),
        }
