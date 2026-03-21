from __future__ import annotations

from typing import Any


def promote_working_to_episodic(state) -> list[dict]:
    state.memory.setdefault("working", {})
    episodic = state.memory.setdefault("episodic", [])

    promoted: list[dict] = []

    candidate = {
        "goal": getattr(state, "goal", None),
        "plan": getattr(state, "plan", None),
        "final_output": getattr(state, "final_output", None),
        "critique": state.critique.model_dump() if getattr(state, "critique", None) else None,
        "run_id": getattr(state.runtime, "run_id", "unknown")
        if hasattr(state, "runtime")
        else "unknown",
        "flow_name": getattr(state.runtime, "flow_name", "unknown")
        if hasattr(state, "runtime")
        else "unknown",
    }

    important = bool(candidate["final_output"]) or bool(candidate["plan"])
    if hasattr(state, "runtime") and getattr(state.runtime, "degraded", False):
        important = True

    if important:
        episodic.append(candidate)
        promoted.append(candidate)

    return promoted


def promote_episodic_to_semantic(memory_store: dict[str, Any]) -> list[dict]:
    episodic = memory_store.setdefault("episodic", [])
    semantic = memory_store.setdefault("semantic", [])

    promoted: list[dict] = []
    for episode in episodic:
        if episode.get("final_output") and episode not in semantic:
            item = {
                "kind": "validated_output_pattern",
                "flow_name": episode.get("flow_name"),
                "run_id": episode.get("run_id"),
            }
            semantic.append(item)
            promoted.append(item)

    return promoted
