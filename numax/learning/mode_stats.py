from __future__ import annotations

from typing import Any, Dict, List

from numax.learning.mode_feedback import load_mode_feedback


from dataclasses import dataclass, field

@dataclass
class ModeFeedback:
    run_id: str
    target_id: str
    target_type: str
    success: bool = True
    rollback: bool = False
    duration_seconds: float = 0.0
    cost_used_usd: float = 0.0
    retries: int = 0
    quality_score: float = 0.0
    metrics: Dict[str, Any] = field(default_factory=dict)

    def model_dump(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "target_id": self.target_id,
            "target_type": self.target_type,
            "success": self.success,
            "rollback": self.rollback,
            "duration_seconds": self.duration_seconds,
            "cost_used_usd": self.cost_used_usd,
            "retries": self.retries,
            "quality_score": self.quality_score,
            "metrics": self.metrics,
        }


class ModeStatsAggregator:
    def __init__(self, history: List[ModeFeedback]) -> None:
        self.history = history

    def get_all_summaries(self) -> Dict[str, Any]:
        return compute_mode_stats()


def build_mock_history() -> List[ModeFeedback]:
    return [
        ModeFeedback(run_id="m11", target_id="repo_operator", target_type="profile", success=True, quality_score=0.9),
        ModeFeedback(run_id="m12", target_id="research_mode", target_type="profile", success=True, quality_score=0.8),
        ModeFeedback(run_id="m13", target_id="workspace_audit", target_type="recipe", success=True, quality_score=0.95),
    ]


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
