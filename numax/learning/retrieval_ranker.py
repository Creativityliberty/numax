from __future__ import annotations

import json
from pathlib import Path
from typing import Any

RANKER_POLICY_PATH = Path("data/state/retrieval_ranker_feedback.json")
RANKER_POLICY_PATH.parent.mkdir(parents=True, exist_ok=True)

DEFAULT_RANKER_POLICY: dict[str, Any] = {
    "source_boosts": {},
}


def load_ranker_policy() -> dict[str, Any]:
    if not RANKER_POLICY_PATH.exists():
        return dict(DEFAULT_RANKER_POLICY)
    try:
        data = json.loads(RANKER_POLICY_PATH.read_text(encoding="utf-8"))
        return {**DEFAULT_RANKER_POLICY, **(data or {})}
    except Exception:
        return dict(DEFAULT_RANKER_POLICY)


def save_ranker_policy(policy: dict[str, Any]) -> None:
    RANKER_POLICY_PATH.write_text(json.dumps(policy, indent=2), encoding="utf-8")


def rerank_results(results: list[dict]) -> list[dict]:
    policy = load_ranker_policy()
    boosts = policy.get("source_boosts", {})

    enriched = []
    for item in results:
        source_id = item.get("source_id", "")
        base_score = float(item.get("score", 0.0))
        boost = float(boosts.get(source_id, 0.0))
        updated = dict(item)
        updated["score"] = base_score + boost
        enriched.append(updated)

    enriched.sort(key=lambda x: float(x.get("score", 0.0)), reverse=True)
    return enriched
