from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def apply_text_patch(
    path: str,
    old_text: str,
    new_text: str,
    preview_only: bool = True,
    encoding: str = "utf-8",
) -> Dict[str, Any]:
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
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "path": str(target),
        }

    if old_text not in content:
        return {
            "ok": False,
            "error": "old_text_not_found",
            "path": str(target),
        }

    updated = content.replace(old_text, new_text, 1)

    if not preview_only:
        try:
            target.write_text(updated, encoding=encoding)
        except Exception as exc:
            return {
                "ok": False,
                "error": str(exc),
                "path": str(target),
            }

    return {
        "ok": True,
        "path": str(target),
        "preview_only": preview_only,
        "before_excerpt": old_text[:500],
        "after_excerpt": new_text[:500],
        "changed": True,
    }
