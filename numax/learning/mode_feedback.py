from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


MODE_FEEDBACK_PATH = Path("/Volumes/Numtema/numax/data/state/mode_feedback.json")
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
def capture_run_feedback(**kwargs: Any) -> Any:
    # Minimal version for demonstration nodes consistency
    from numax.learning.mode_stats import ModeFeedback
    record = {
        "run_id": kwargs.get("run_id", "unknown"),
        "target_id": kwargs.get("target_id", "unknown"),
        "target_type": kwargs.get("target_type", "unknown"),
        "success": kwargs.get("ok", True),
        "quality_score": kwargs.get("metrics", {}).get("quality_score", 0.7),
    }
    # Backward compatibility with mode_stats.py
    if record["target_type"] == "profile":
        record["profile"] = record["target_id"]
    elif record["target_type"] == "recipe":
        record["recipe"] = record["target_id"]

    append_mode_feedback(record)
    # Filter for dataclass
    clean_record = {k: v for k, v in record.items() if k not in ["profile", "recipe"]}
    return ModeFeedback(**clean_record)
