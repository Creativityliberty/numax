from __future__ import annotations

from typing import Any, Dict

KNOWN_EVENT_KINDS = {
    "trace",
    "provider",
    "tool",
    "critic",
    "budget",
    "job",
    "sandbox",
    "unknown",
}


def guard_event(event: Dict[str, Any]) -> Dict[str, Any]:
    kind = event.get("kind", "unknown")
    if kind not in KNOWN_EVENT_KINDS:
        return {
            "kind": "unknown",
            "name": event.get("name", "unknown_event"),
            "payload": {
                "original_kind": kind,
                "original_event": event,
            },
            "severity": "warning",
            "guarded": True,
        }

    return {
        **event,
        "guarded": False,
    }
