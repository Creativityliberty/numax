from __future__ import annotations

from typing import Any


def get_baseline() -> dict:
    return {
        "baseline_id": "llm_tools",
        "description": "LLM plus simple tools baseline without full governance or continuity.",
    }


def run_baseline(scenario: dict[str, Any]) -> dict[str, Any]:
    uses_retrieval = (
        "search" in scenario["prompt"].lower() or "memory" in scenario["prompt"].lower()
    )

    return {
        "scenario_id": scenario["scenario_id"],
        "system": "llm_tools",
        "flow": "tool_augmented",
        "task_success": True,
        "artifact_valid": False,
        "recovered": not scenario.get("inject_failure", False),
        "continuity_score": 0.15 if scenario.get("requires_resume") else 0.35,
        "cost_used_usd": 0.03,
        "tokens_used": 650,
        "rollback_ok": False,
        "replay_ok": False,
        "trace_count": 0,
        "fsm_state": "N/A",
        "has_plan": uses_retrieval,
        "final_output": {"text": f"[llm_tools] response to: {scenario['prompt']}"},
        "artifact": None,
    }
