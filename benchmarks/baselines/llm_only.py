from __future__ import annotations

from typing import Any


def get_baseline() -> dict:
    return {
        "baseline_id": "llm_only",
        "description": "Single LLM-style direct answer baseline without retrieval/planning/artifact governance.",
    }


def run_baseline(scenario: dict[str, Any]) -> dict[str, Any]:
    text = f"[llm_only] direct response to: {scenario['prompt']}"
    return {
        "scenario_id": scenario["scenario_id"],
        "system": "llm_only",
        "flow": "direct",
        "task_success": True,
        "artifact_valid": False,
        "recovered": not scenario.get("inject_failure", False),
        "continuity_score": 0.1 if scenario.get("requires_resume") else 0.3,
        "cost_used_usd": 0.02,
        "tokens_used": 500,
        "rollback_ok": False,
        "replay_ok": False,
        "trace_count": 0,
        "fsm_state": "N/A",
        "has_plan": False,
        "final_output": {"text": text},
        "artifact": None,
    }
