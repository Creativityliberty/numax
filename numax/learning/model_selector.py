from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from numax.bootstrap import build_model_catalog, build_model_resolver

MODEL_SELECTOR_PATH = Path("data/state/model_selector_feedback.json")
MODEL_SELECTOR_PATH.parent.mkdir(parents=True, exist_ok=True)

DEFAULT_SELECTOR_POLICY: dict[str, Any] = {
    "prefer_by_role": {},
    "avoid_models": [],
}


def load_model_selector_policy() -> dict[str, Any]:
    if not MODEL_SELECTOR_PATH.exists():
        return dict(DEFAULT_SELECTOR_POLICY)
    try:
        data = json.loads(MODEL_SELECTOR_PATH.read_text(encoding="utf-8"))
        return {**DEFAULT_SELECTOR_POLICY, **(data or {})}
    except Exception:
        return dict(DEFAULT_SELECTOR_POLICY)


def save_model_selector_policy(policy: dict[str, Any]) -> None:
    MODEL_SELECTOR_PATH.write_text(json.dumps(policy, indent=2), encoding="utf-8")


def select_model_for_role(role: str) -> dict:
    policy = load_model_selector_policy()
    catalog = build_model_catalog()
    resolver = build_model_resolver(catalog)

    preferred = policy.get("prefer_by_role", {}).get(role)
    avoid = set(policy.get("avoid_models", []))

    if preferred and preferred not in avoid:
        spec = catalog.get(preferred)
        if spec and spec.status == "enabled":
            return spec.model_dump()

    spec = resolver.resolve(role=role)
    if spec.id not in avoid:
        return spec.model_dump()

    candidates = [m for m in catalog.list_by_role(role) if m.id not in avoid]
    if candidates:
        return candidates[0].model_dump()

    return spec.model_dump()
