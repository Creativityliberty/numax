from __future__ import annotations

from typing import Any


def get_baseline() -> dict:
    return {
        "baseline_id": "llm_tools_memory",
        "description": "LLM plus tools plus light memory baseline without full mutation/governance stack.",
    }


def run_baseline(scenario: dict[str, Any]) -> dict[str, Any]:
    continuity_score = 0.45 if scenario.get("requires_resume") else 0.4
    if scenario.get("inject_retrieved_context"):
        continuity_score += 0.1

    return {
        "scenario_id": scenario["scenario_id"],
        "system": "llm_tools_memory",
        "flow": "tool_memory_augmented",
        "task_success": True,
        "artifact_valid": False,
        "recovered": not scenario.get("inject_failure", False),
        "continuity_score": min(1.0, continuity_score),
        "cost_used_usd": 0.035,
        "tokens_used": 720,
        "rollback_ok": False,
        "replay_ok": False,
        "trace_count": 0,
        "fsm_state": "N/A",
        "has_plan": True,
        "final_output": {"text": f"[llm_tools_memory] response to: {scenario['prompt']}"},
        "artifact": None,
        "promoted_episodic_count": 0,
        "semantic_count": 0,
        "memory_policy": {},
        "mutation_notes": [],
    }
