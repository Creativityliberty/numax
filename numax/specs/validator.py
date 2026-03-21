from __future__ import annotations

from typing import Any, Dict

from numax.specs.assumption_map import AssumptionMap
from numax.specs.intent_spec import IntentSpec
from numax.specs.work_spec import WorkSpec


def validate_spec_bundle(
    intent_spec: IntentSpec,
    work_spec: WorkSpec,
    assumption_map: AssumptionMap,
) -> Dict[str, Any]:
    notes: list[str] = []
    ok = True
    confidence = 0.85

    if not intent_spec.objective.strip():
        ok = False
        confidence = 0.2
        notes.append("Intent objective is empty.")

    if not work_spec.deliverables:
        ok = False
        confidence = min(confidence, 0.35)
        notes.append("No deliverables defined.")

    if not work_spec.acceptance_criteria:
        ok = False
        confidence = min(confidence, 0.35)
        notes.append("No acceptance criteria defined.")

    high_risk_unverified = [
        item for item in assumption_map.items
        if item.status == "unverified" and item.impact == "high"
    ]
    if high_risk_unverified:
        ok = False
        confidence = min(confidence, 0.40)
        notes.append("High-impact assumptions remain unverified.")

    if intent_spec.ambiguity_level == "high":
        confidence -= 0.15
        notes.append("Intent ambiguity is high.")

    confidence = max(0.0, min(1.0, confidence))

    return {
        "ok": ok,
        "confidence": confidence,
        "notes": notes,
    }
