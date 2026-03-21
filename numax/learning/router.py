from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROUTER_FEEDBACK_PATH = Path("data/state/router_feedback.json")
ROUTER_FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)

DEFAULT_ROUTER_POLICY = {
    "retrieve_keywords": [
        "source",
        "document",
        "file",
        "reference",
        "citation",
        "research",
        "search",
        "look up",
    ],
    "prefer_retrieve_if_context_missing": True,
}


def load_router_policy() -> dict[str, Any]:
    if not ROUTER_FEEDBACK_PATH.exists():
        return dict(DEFAULT_ROUTER_POLICY)
    try:
        data = json.loads(ROUTER_FEEDBACK_PATH.read_text(encoding="utf-8"))
        return {**DEFAULT_ROUTER_POLICY, **(data or {})}
    except Exception:
        return dict(DEFAULT_ROUTER_POLICY)


def save_router_policy(policy: dict[str, Any]) -> None:
    ROUTER_FEEDBACK_PATH.write_text(json.dumps(policy, indent=2), encoding="utf-8")


def route_intent_adaptive(user_input: str, has_context: bool) -> dict[str, Any]:
    policy = load_router_policy()
    text = user_input.strip().lower()
    keywords = policy.get("retrieve_keywords", [])

    if any(keyword in text for keyword in keywords):
        return {
            "route": "retrieve",
            "understanding_confidence": 0.85,
            "routing_policy": "keyword_match",
        }

    return {
        "route": "answer",
        "understanding_confidence": 0.70,
        "routing_policy": "default",
    }


def update_router_policy(feedback: dict[str, Any]) -> dict[str, Any]:
    policy = load_router_policy()
    add_keywords = feedback.get("add_retrieve_keywords", [])
    if add_keywords:
        merged = set(policy.get("retrieve_keywords", []))
        merged.update(str(x).lower() for x in add_keywords)
        policy["retrieve_keywords"] = sorted(list(merged))
    save_router_policy(policy)
    return policy
