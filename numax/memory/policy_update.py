from __future__ import annotations

from typing import Any


def update_memory_policy_from_history(memory_store: dict[str, Any]) -> dict[str, Any]:
    history = memory_store.setdefault("tool_history", [])
    policy = memory_store.setdefault("memory_policy", {})

    failures = sum(1 for item in history if item.get("ok") is False)
    successes = sum(1 for item in history if item.get("ok") is True)

    policy["history_failures"] = failures
    policy["history_successes"] = successes
    policy["prefer_conservative_promotion"] = failures > successes

    return policy
