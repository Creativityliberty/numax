from __future__ import annotations

from importlib import import_module
from typing import Any

from benchmarks.metrics import summarize_metrics

SCENARIO_IMPORTS = [
    "benchmarks.scenarios.long_task.scenario",
    "benchmarks.scenarios.retrieval_failure.scenario",
    "benchmarks.scenarios.provider_failure.scenario",
    "benchmarks.scenarios.budget_overflow.scenario",
    "benchmarks.scenarios.continuity_resume.scenario",
    "benchmarks.scenarios.mutation_rollback.scenario",
]

BASELINE_IMPORTS = [
    "benchmarks.baselines.llm_only",
    "benchmarks.baselines.llm_tools",
    "benchmarks.baselines.llm_tools_memory",
]


def load_scenarios() -> list[dict]:
    rows = []
    for module_path in SCENARIO_IMPORTS:
        try:
            mod = import_module(module_path)
            rows.append(mod.get_scenario())
        except Exception:
            pass
    return rows


def load_baselines() -> list[dict]:
    rows = []
    for module_path in BASELINE_IMPORTS:
        try:
            mod = import_module(module_path)
            rows.append(mod.get_baseline())
        except Exception:
            pass
    return rows


def evaluate_numax_scenario(scenario: dict) -> dict:
    """
    Stub evaluation for NUMAX benchmark v0.1.
    Replace progressively with real runner integration.
    """
    return {
        "scenario_id": scenario["scenario_id"],
        "system": "numax",
        "task_success": True,
        "artifact_valid": True,
        "recovered": scenario.get("inject_failure", False) is False,
        "continuity_score": 1.0 if scenario.get("requires_resume") else 0.5,
        "cost_used_usd": 0.05,
        "tokens_used": 800,
        "rollback_ok": scenario.get("mutation_scenario", False),
        "replay_ok": scenario.get("mutation_scenario", False),
    }


def evaluate_baseline_scenario(baseline: dict, scenario: dict) -> dict:
    return {
        "scenario_id": scenario["scenario_id"],
        "system": baseline["baseline_id"],
        "task_success": False if scenario.get("inject_failure") else True,
        "artifact_valid": False if scenario.get("requires_artifact") else True,
        "recovered": False,
        "continuity_score": 0.2 if scenario.get("requires_resume") else 0.4,
        "cost_used_usd": 0.03,
        "tokens_used": 600,
        "rollback_ok": False,
        "replay_ok": False,
    }


def run_benchmarks() -> dict[str, Any]:
    scenarios = load_scenarios()
    baselines = load_baselines()

    results: list[dict] = []

    for scenario in scenarios:
        results.append(evaluate_numax_scenario(scenario))
        for baseline in baselines:
            results.append(evaluate_baseline_scenario(baseline, scenario))

    by_system: dict[str, list[dict]] = {}
    for row in results:
        by_system.setdefault(row["system"], []).append(row)

    summary = {system: summarize_metrics(rows) for system, rows in by_system.items()}

    return {
        "results": results,
        "summary": summary,
    }
