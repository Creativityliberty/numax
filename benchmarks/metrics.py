from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def task_success_rate(results: Iterable[dict]) -> float:
    rows = list(results)
    if not rows:
        return 0.0
    success = sum(1 for row in rows if row.get("task_success") is True)
    return success / len(rows)


def artifact_validity_rate(results: Iterable[dict]) -> float:
    rows = list(results)
    if not rows:
        return 0.0
    valid = sum(1 for row in rows if row.get("artifact_valid") is True)
    return valid / len(rows)


def recovery_success_rate(results: Iterable[dict]) -> float:
    rows = list(results)
    if not rows:
        return 0.0
    recovered = sum(1 for row in rows if row.get("recovered") is True)
    return recovered / len(rows)


def continuity_resume_score(results: Iterable[dict]) -> float:
    rows = list(results)
    if not rows:
        return 0.0
    values = [float(row.get("continuity_score", 0.0)) for row in rows]
    return sum(values) / len(values)


def budget_efficiency_score(results: Iterable[dict]) -> float:
    rows = list(results)
    if not rows:
        return 0.0

    scores = []
    for row in rows:
        success = 1.0 if row.get("task_success") else 0.0
        cost = float(row.get("cost_used_usd", 0.0))
        tokens = float(row.get("tokens_used", 0.0))
        denominator = 1.0 + cost + (tokens / 10000.0)
        scores.append(success / denominator)

    return sum(scores) / len(scores)


def mutation_safety_score(results: Iterable[dict]) -> float:
    rows = list(results)
    if not rows:
        return 0.0

    safe = 0
    for row in rows:
        rollback_ok = row.get("rollback_ok", False)
        replay_ok = row.get("replay_ok", False)
        if rollback_ok or replay_ok:
            safe += 1
    return safe / len(rows)


def summarize_metrics(results: Iterable[dict]) -> dict[str, Any]:
    rows = list(results)
    return {
        "task_success_rate": task_success_rate(rows),
        "artifact_validity_rate": artifact_validity_rate(rows),
        "recovery_success_rate": recovery_success_rate(rows),
        "continuity_resume_score": continuity_resume_score(rows),
        "budget_efficiency_score": budget_efficiency_score(rows),
        "mutation_safety_score": mutation_safety_score(rows),
        "count": len(rows),
    }
