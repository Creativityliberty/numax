from __future__ import annotations

import json
from pathlib import Path

from numax.core.state import NumaxState


def save_continuity_state(state: NumaxState, path: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "goal": state.goal,
        "memory": state.memory,
        "runtime": state.runtime.model_dump(),
        "budget": state.budget.model_dump(),
        "confidence": state.confidence.model_dump(),
    }

    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    state.add_trace("continuity", "post", "Continuity state saved", path=str(target))


def load_continuity_state(path: str) -> dict | None:
    target = Path(path)
    if not target.exists():
        return None
    return json.loads(target.read_text(encoding="utf-8"))  # type: ignore


def restore_continuity(state: NumaxState, path: str) -> NumaxState:
    payload = load_continuity_state(path)
    if payload is None:
        state.add_trace("continuity", "post", "No continuity state found", path=path)
        return state

    state.goal = payload.get("goal", {})
    state.memory = payload.get("memory", {"working": {}, "continuity": {}})

    continuity_meta = state.memory.setdefault("continuity", {})
    continuity_meta["restored_from"] = path
    continuity_meta["restored"] = True

    state.add_trace("continuity", "post", "Continuity restored", path=path)
    return state
