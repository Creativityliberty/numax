from __future__ import annotations

from typing import Any


def consolidate_patterns(memory_store: dict[str, Any]) -> dict[str, Any]:
    episodic = memory_store.setdefault("episodic", [])
    semantic = memory_store.setdefault("semantic", [])

    seen = {(item.get("kind"), item.get("flow_name")) for item in semantic}

    for episode in episodic:
        key = ("validated_output_pattern", episode.get("flow_name"))
        if episode.get("final_output") and key not in seen:
            semantic.append(
                {
                    "kind": "validated_output_pattern",
                    "flow_name": episode.get("flow_name"),
                    "run_id": episode.get("run_id"),
                }
            )
            seen.add(key)

    return memory_store
