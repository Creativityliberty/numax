from __future__ import annotations

from typing import Any, Dict

from numax.learning.mode_stats import compute_mode_stats


def select_best_mode(
    group_by: str = "profile",
    min_runs: int = 1,
) -> Dict[str, Any]:
    result = compute_mode_stats(group_by=group_by)
    stats = result["stats"]

    best_key = None
    best_score = -1.0

    for key, row in stats.items():
        runs = row.get("runs", 0)
        if runs < min_runs:
            continue

        score = (
            row.get("success_rate", 0.0) * 0.45
            + row.get("avg_quality_score", 0.0) * 0.30
            + (1.0 - row.get("rollback_rate", 0.0)) * 0.15
            + max(0.0, 1.0 - min(row.get("avg_retries", 0.0) / 5.0, 1.0)) * 0.10
        )

        if score > best_score:
            best_score = score
            best_key = key

    return {
        "group_by": group_by,
        "selected": best_key,
        "score": best_score if best_key is not None else 0.0,
        "stats": stats,
    }


class SmartModeSelector:
    def __init__(self, history: list) -> None:
        self.history = history

    def recommend(self, task_type: str, candidates: list[str]) -> Dict[str, Any]:
        # Weighted recommendation based on history/mock stats
        from numax.learning.mode_stats import compute_mode_stats
        
        # In this demo version, we use compute_mode_stats internally
        report = compute_mode_stats(group_by="profile")
        stats = report["stats"]
        
        best_candidate = candidates[0] if candidates else "repo_operator"
        best_score = -1.0
        
        for cand in candidates:
            score = 0.5 # Default
            if cand in stats:
                row = stats[cand]
                score = row.get("success_rate", 0.0) * 0.7 + row.get("avg_quality_score", 0.0) * 0.3
            
            if score > best_score:
                best_score = score
                best_candidate = cand
        
        return {
            "task_type": task_type,
            "recommended_id": best_candidate,
            "confidence": best_score,
            "reason": "Highest historical success/quality score",
        }
