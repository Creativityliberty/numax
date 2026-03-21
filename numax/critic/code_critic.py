from __future__ import annotations

from typing import Any, Dict, List


CRITICAL_PATH_HINTS = {
    "pyproject.toml",
    "package.json",
    "requirements.txt",
    "configs/",
    "numax/core/",
    "numax/governance/",
    "numax/guardian/",
}


def _is_critical_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    for hint in CRITICAL_PATH_HINTS:
        if hint.endswith("/"):
            if normalized.startswith(hint):
                return True
        elif normalized == hint or normalized.endswith("/" + hint):
            return True
    return False


def review_code_change(
    patch: Dict[str, Any] | None,
    test_result: Dict[str, Any] | None,
    active_files: List[str] | None = None,
) -> Dict[str, Any]:
    patch = patch or {}
    test_result = test_result or {}
    active_files = active_files or []

    notes: List[str] = []
    decision = "accept"
    confidence = 0.80
    risk = "low"
    scope = "narrow"

    proposal_path = patch.get("path")
    apply_result = patch.get("apply_result", {})
    preview_only = apply_result.get("preview_only", True)

    if not proposal_path:
        decision = "revise"
        confidence = 0.20
        risk = "medium"
        notes.append("No patch target path found.")
        return {
            "decision": decision,
            "confidence": confidence,
            "risk": risk,
            "scope": scope,
            "notes": notes,
        }

    if len(active_files) > 3:
        scope = "medium"
    if len(active_files) > 10:
        scope = "wide"
        notes.append("Many files are involved in the current workspace focus.")

    if _is_critical_path(proposal_path):
        risk = "high"
        confidence -= 0.10
        notes.append("Patch touches a critical path.")

    if not apply_result.get("ok", False):
        decision = "revise"
        confidence = 0.25
        risk = "high"
        notes.append("Patch application failed.")
        return {
            "decision": decision,
            "confidence": confidence,
            "risk": risk,
            "scope": scope,
            "notes": notes,
        }

    if preview_only:
        confidence -= 0.05
        notes.append("Patch was only previewed, not applied for real.")

    if not test_result:
        decision = "revise"
        confidence = min(confidence, 0.45)
        risk = max(risk, "medium")
        notes.append("No test result available.")
    else:
        if not test_result.get("ok", False):
            decision = "revert" if not preview_only else "revise"
            confidence = 0.90
            risk = "high"
            notes.append("Tests failed after the proposed change.")
        else:
            notes.append("Tests passed.")
            confidence += 0.05

    before_excerpt = apply_result.get("before_excerpt", "") or ""
    after_excerpt = apply_result.get("after_excerpt", "") or ""
    if before_excerpt == after_excerpt:
        decision = "revise"
        confidence = min(confidence, 0.35)
        notes.append("Patch does not appear to change content materially.")

    confidence = max(0.0, min(1.0, confidence))

    return {
        "decision": decision,   # accept | revise | revert
        "confidence": confidence,
        "risk": risk,           # low | medium | high
        "scope": scope,         # narrow | medium | wide
        "notes": notes,
    }
