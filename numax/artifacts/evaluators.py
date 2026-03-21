from __future__ import annotations

from typing import Any, Dict


def evaluate_artifact(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload.get("text", "") or "")
    trace = payload.get("trace", []) or []

    completeness = 1.0 if text else 0.0
    traceability = 1.0 if trace else 0.5
    structure = 1.0 if isinstance(payload, dict) else 0.5
    exploitability = 1.0 if len(text.split()) >= 5 else 0.4

    overall = (completeness + traceability + structure + exploitability) / 4.0

    return {
        "completeness": completeness,
        "traceability": traceability,
        "structure": structure,
        "exploitability": exploitability,
        "overall": overall,
    }
