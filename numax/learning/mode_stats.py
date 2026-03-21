from __future__ import annotations

from typing import Any, Dict, List

from numax.learning.mode_feedback import load_mode_feedback


def _safe_avg(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def compute_mode_stats(group_by: str = "profile") -> Dict[str, Any]:
    payload = load_mode_feedback()
    records = payload.get("records", [])

    grouped: Dict[str, list[dict]] = {}
    for record in records:
        key = record.get(group_by) or "unknown"
        grouped.setdefault(key, []).append(record)

    stats: Dict[str, Any] = {}

    for key, items in grouped.items():
        total = len(items)
        success = sum(1 for item in items if item.get("success") is True)
        rollback = sum(1 for item in items if item.get("rollback") is True)
        durations = [float(item.get("duration_seconds", 0.0)) for item in items]
        costs = [float(item.get("cost_used_usd", 0.0)) for item in items]
        retries = [float(item.get("retries", 0)) for item in items]
        qualities = [float(item.get("quality_score", 0.0)) for item in items]

        stats[key] = {
            "runs": total,
            "success_rate": success / total if total else 0.0,
            "rollback_rate": rollback / total if total else 0.0,
            "avg_duration_seconds": _safe_avg(durations),
            "avg_cost_usd": _safe_avg(costs),
            "avg_retries": _safe_avg(retries),
            "avg_quality_score": _safe_avg(qualities),
        }

    return {
        "group_by": group_by,
        "stats": stats,
    }
