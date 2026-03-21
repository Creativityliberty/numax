from __future__ import annotations

from typing import Any


def forget_low_value_items(memory_store: dict[str, Any]) -> dict[str, Any]:
    episodic = memory_store.setdefault("episodic", [])

    filtered = []
    for item in episodic:
        has_signal = bool(item.get("final_output") or item.get("plan") or item.get("goal"))
        if has_signal:
            filtered.append(item)

    memory_store["episodic"] = filtered
    return memory_store
