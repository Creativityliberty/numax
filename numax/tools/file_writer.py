from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def write_file(
    path: str,
    content: str,
    overwrite: bool = False,
    encoding: str = "utf-8",
) -> Dict[str, Any]:
    target = Path(path).resolve()

    if target.exists() and not overwrite:
        return {
            "ok": False,
            "error": "file_exists_overwrite_required",
            "path": str(target),
        }

    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding=encoding)
        return {
            "ok": True,
            "path": str(target),
            "size_bytes": target.stat().st_size,
            "overwrote": target.exists(),
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "path": str(target),
        }
