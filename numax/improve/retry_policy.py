from __future__ import annotations

from typing import Any, Dict, List


def decide_retry_policy(
    suggestions: List[dict],
    retries: int,
    max_retries: int = 3,
) -> Dict[str, Any]:
    if retries >= max_retries:
        return {
            "decision": "stop",
            "reason": "Retry budget exhausted.",
            "retry_allowed": False,
        }

    types = {item.get("type") for item in suggestions}

    if "clarify_spec" in types:
        return {
            "decision": "replan",
            "reason": "Spec must be clarified before continuing.",
            "retry_allowed": True,
        }

    if "repair_after_test_failure" in types:
        return {
            "decision": "retry",
            "reason": "A repair loop is justified after failing tests.",
            "retry_allowed": True,
        }

    if "revise_patch" in types:
        return {
            "decision": "retry",
            "reason": "A patch revision loop is justified.",
            "retry_allowed": True,
        }

    if "revert_patch" in types:
        return {
            "decision": "replan",
            "reason": "Patch should be reverted and the task replanned.",
            "retry_allowed": True,
        }

    return {
        "decision": "stop",
        "reason": "No strong retry/replan signal.",
        "retry_allowed": False,
    }
