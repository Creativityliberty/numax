from __future__ import annotations

from typing import Any, Dict, List


def suggest_improvements(state_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    suggestions: List[dict] = []

    last_test_run = state_snapshot.get("last_test_run", {}) or {}
    code_review = state_snapshot.get("code_review", {}) or {}
    spec_validation = state_snapshot.get("spec_validation", {}) or {}
    last_failure = state_snapshot.get("last_failure", {}) or {}
    next_action = state_snapshot.get("next_recommended_action")

    if spec_validation and not spec_validation.get("ok", False):
        suggestions.append(
            {
                "type": "clarify_spec",
                "priority": "high",
                "reason": "Spec validation failed or remains too weak.",
            }
        )

    if last_test_run and not last_test_run.get("ok", False):
        suggestions.append(
            {
                "type": "repair_after_test_failure",
                "priority": "high",
                "reason": "Latest test run failed.",
            }
        )

    if code_review:
        decision = code_review.get("decision")
        if decision == "revise":
            suggestions.append(
                {
                    "type": "revise_patch",
                    "priority": "medium",
                    "reason": "Code critic recommends revision.",
                }
            )
        elif decision == "revert":
            suggestions.append(
                {
                    "type": "revert_patch",
                    "priority": "high",
                    "reason": "Code critic recommends revert.",
                }
            )

    if last_failure and not suggestions:
        suggestions.append(
            {
                "type": "inspect_failure",
                "priority": "medium",
                "reason": "A failure is recorded but no explicit improvement path exists.",
            }
        )

    if not suggestions and next_action:
        suggestions.append(
            {
                "type": "follow_next_action",
                "priority": "low",
                "reason": f"Use next recommended action: {next_action}",
            }
        )

    if not suggestions:
        suggestions.append(
            {
                "type": "stop",
                "priority": "low",
                "reason": "No strong improvement signal detected.",
            }
        )

    return {
        "ok": True,
        "suggestions": suggestions,
    }
