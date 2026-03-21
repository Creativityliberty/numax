from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from numax.core.state import NumaxState

TRACE_DIR = Path("data/traces")
TRACE_DIR.mkdir(parents=True, exist_ok=True)


def _json_safe(value: Any) -> Any:
    try:
        json.dumps(value)
        return value
    except TypeError:
        return str(value)


def save_run_trace(state: NumaxState) -> str:
    run_id = state.runtime.run_id or "unknown-run"
    path = TRACE_DIR / f"{run_id}.jsonl"

    with path.open("w", encoding="utf-8") as f:
        for event in state.trace:
            row = {
                "run_id": run_id,
                "flow_name": state.runtime.flow_name,
                "fsm_state": state.runtime.fsm_state,
                "node": event.node,
                "phase": event.phase,
                "message": event.message,
                "data": _json_safe(event.data),
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    return str(path)


def load_run_trace(run_id: str) -> list[dict]:
    path = TRACE_DIR / f"{run_id}.jsonl"
    if not path.exists():
        return []

    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows
