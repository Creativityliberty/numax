from __future__ import annotations

from pathlib import Path


def is_path_allowed(path: str, allowed_roots: list[str] | None = None) -> bool:
    allowed_roots = allowed_roots or ["."]
    target = Path(path).resolve()
    for root in allowed_roots:
        root_path = Path(root).resolve()
        try:
            target.relative_to(root_path)
            return True
        except Exception:
            continue
    return False
