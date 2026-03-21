from __future__ import annotations

from typing import Any, Dict, List


def evaluate_mutation_gate(
    suggestions: List[dict],
    safety_confidence: float,
    degraded: bool,
) -> Dict[str, Any]:
    high_priority = [item for item in suggestions if item.get("priority") == "high"]

    if degraded:
        return {
            "allowed": False,
            "mode": "blocked",
            "reason": "Runtime is degraded; do not mutate automatically.",
        }

    if safety_confidence < 0.6:
        return {
            "allowed": False,
            "mode": "blocked",
            "reason": "Safety confidence is too low.",
        }

    if high_priority:
        return {
            "allowed": True,
            "mode": "gated",
            "reason": "High-priority improvements may proceed under review.",
        }

    return {
        "allowed": True,
        "mode": "light",
        "reason": "Only low/medium-priority suggestions detected.",
    }
