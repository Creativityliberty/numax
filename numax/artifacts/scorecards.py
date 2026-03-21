from __future__ import annotations


def build_scorecard(name: str, scores: dict) -> dict:
    return {
        "name": name,
        "scores": scores,
        "verdict": "good" if scores.get("overall", 0.0) >= 0.7 else "weak",
    }
