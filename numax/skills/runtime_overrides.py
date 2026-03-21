from __future__ import annotations

import json
from pathlib import Path
from typing import Any

RUNTIME_OVERRIDES_PATH = Path("data/state/runtime_overrides.json")
RUNTIME_OVERRIDES_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_runtime_overrides() -> dict[str, Any]:
    if not RUNTIME_OVERRIDES_PATH.exists():
        return {}
    try:
        data = json.loads(RUNTIME_OVERRIDES_PATH.read_text(encoding="utf-8"))
        # type cast
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_runtime_overrides(overrides: dict[str, Any]) -> None:
    RUNTIME_OVERRIDES_PATH.write_text(json.dumps(overrides, indent=2), encoding="utf-8")


def set_nested_value(obj: dict[str, Any], dotted_path: str, value: Any) -> dict[str, Any]:
    parts = dotted_path.split(".")
    cursor = obj
    for part in parts[:-1]:
        # Using cast to please mypy since dict can be nested
        cursor = cursor.setdefault(part, {})
    cursor[parts[-1]] = value
    return obj
