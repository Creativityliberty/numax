from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from numax.learning.critic_calibration import load_critic_policy, save_critic_policy
from numax.learning.model_selector import load_model_selector_policy, save_model_selector_policy
from numax.learning.retrieval_ranker import load_ranker_policy, save_ranker_policy
from numax.learning.router import load_router_policy, save_router_policy

FEEDBACK_LOG_PATH = Path("data/state/policy_feedback_log.jsonl")
FEEDBACK_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def record_feedback(feedback: dict[str, Any]) -> None:
    with FEEDBACK_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(feedback, ensure_ascii=False) + "\n")


def apply_feedback(feedback: dict[str, Any]) -> dict[str, Any]:
    record_feedback(feedback)
    target = feedback.get("target")

    if target == "router":
        policy = load_router_policy()
        add_keywords = feedback.get("add_retrieve_keywords", [])
        if add_keywords:
            merged = set(policy.get("retrieve_keywords", []))
            merged.update(str(x).lower() for x in add_keywords)
            policy["retrieve_keywords"] = sorted(list(merged))
        save_router_policy(policy)
        return {"router": policy}

    if target == "model_selector":
        policy = load_model_selector_policy()
        role = feedback.get("role")
        model_id = feedback.get("prefer_model_id")
        if role and model_id:
            prefer = policy.setdefault("prefer_by_role", {})
            prefer[str(role)] = str(model_id)
        save_model_selector_policy(policy)
        return {"model_selector": policy}

    if target == "retrieval_ranker":
        policy = load_ranker_policy()
        boosts = policy.setdefault("source_boosts", {})
        source_id = feedback.get("source_id")
        delta = float(feedback.get("delta", 0.0))
        if source_id:
            boosts[str(source_id)] = float(boosts.get(str(source_id), 0.0)) + delta
        save_ranker_policy(policy)
        return {"retrieval_ranker": policy}

    if target == "critic":
        policy = load_critic_policy()
        if "confidence_offset_delta" in feedback:
            policy["confidence_offset"] = float(policy.get("confidence_offset", 0.0)) + float(
                feedback["confidence_offset_delta"]
            )
        if "strict_mode" in feedback:
            policy["strict_mode"] = bool(feedback["strict_mode"])
        save_critic_policy(policy)
        return {"critic": policy}

    return {"noop": True}
