from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


MODE_FEEDBACK_PATH = Path("data/state/mode_feedback.json")
MODE_FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_mode_feedback() -> Dict[str, Any]:
    if not MODE_FEEDBACK_PATH.exists():
        return {"records": []}
    try:
        return json.loads(MODE_FEEDBACK_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"records": []}


def save_mode_feedback(payload: Dict[str, Any]) -> None:
    MODE_FEEDBACK_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def append_mode_feedback(record: Dict[str, Any]) -> None:
    payload = load_mode_feedback()
    payload.setdefault("records", []).append(record)
    save_mode_feedback(payload)
