from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SNAPSHOT_DIR = Path("data/state/skill_snapshots")
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def _snapshot_path(skill_id: str) -> Path:
    safe = skill_id.replace("/", "__")
    return SNAPSHOT_DIR / f"{safe}.json"


def save_skill_snapshot(skill_id: str, payload: dict[str, Any]) -> None:
    _snapshot_path(skill_id).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_skill_snapshot(skill_id: str) -> dict[str, Any]:
    path = _snapshot_path(skill_id)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def delete_skill_snapshot(skill_id: str) -> None:
    path = _snapshot_path(skill_id)
    if path.exists():
        path.unlink()
