from __future__ import annotations

from importlib import import_module
from typing import Any

from benchmarks.metrics import compare_systems, summarize_metrics
from benchmarks.runtime_adapter import run_numax_scenario

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
        mod = import_module(module_path)
        rows.append(mod.get_scenario())
    return rows


def load_baseline_modules() -> list[Any]:
    rows = []
    for module_path in BASELINE_IMPORTS:
        rows.append(import_module(module_path))
    return rows


def run_benchmarks() -> dict[str, Any]:
    scenarios = load_scenarios()
    baselines = load_baseline_modules()

    results: list[dict] = []

    for scenario in scenarios:
        results.append(run_numax_scenario(scenario))
        for baseline in baselines:
            results.append(baseline.run_baseline(scenario))

    by_system: dict[str, list[dict]] = {}
    for row in results:
        by_system.setdefault(row["system"], []).append(row)

    summary = {system: summarize_metrics(rows) for system, rows in by_system.items()}
    comparison = compare_systems(summary)

    return {
        "results": results,
        "summary": comparison["scored"],
        "ranking": comparison["ranking"],
        "winner": comparison["winner"],
    }
