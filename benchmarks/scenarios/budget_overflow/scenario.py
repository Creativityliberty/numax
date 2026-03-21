from __future__ import annotations


def get_scenario() -> dict:
    return {
        "scenario_id": "budget_overflow",
        "flow": "planning_execution",
        "prompt": "Search and deeply explain NUMAX architecture with maximum detail.",
        "max_tokens_total": 5,
        "max_cost_usd": 0.0001,
        "requires_artifact": False,
        "inject_failure": True,
        "requires_resume": False,
        "mutation_scenario": False,
    }
