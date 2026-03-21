from __future__ import annotations

from typing import Any, Dict, List

from numax.runtime.events import RuntimeEvent


def buffer_events(
    events: List[RuntimeEvent],
    max_events: int = 100,
) -> Dict[str, Any]:
    total = len(events)

    if total <= max_events:
        return {
            "events": [event.model_dump() for event in events],
            "truncated": False,
            "kept": total,
            "dropped": 0,
        }

    kept_events = events[-max_events:]
    dropped = total - max_events

    return {
        "events": [event.model_dump() for event in kept_events],
        "truncated": True,
        "kept": len(kept_events),
        "dropped": dropped,
    }
