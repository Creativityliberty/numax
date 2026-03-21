from __future__ import annotations


def artifact_acceptance_policy(scorecard: dict, threshold: float = 0.7) -> dict:
    overall = scorecard.get("scores", {}).get("overall", 0.0)
    return {
        "accepted": overall >= threshold,
        "threshold": threshold,
        "overall": overall,
    }
