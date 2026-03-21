from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from numax.learning.critic_calibration import load_critic_policy, save_critic_policy
from numax.learning.model_selector import load_model_selector_policy, save_model_selector_policy
from numax.learning.router import load_router_policy, save_router_policy
from numax.profiles.registry import build_default_profile_registry
from numax.skills.apply import apply_skill
from numax.skills.runtime_overrides import load_runtime_overrides, save_runtime_overrides


def _deep_merge(base: dict, extra: dict) -> dict:
    result = dict(base)
    for key, value in extra.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


@dataclass
class ProfileApplyResult:
    ok: bool
    profile_id: str
    notes: list[str]


def apply_profile(profile_id: str, preview: bool = True) -> ProfileApplyResult:
    registry = build_default_profile_registry()
    profile = registry.get(profile_id)

    notes: List[str] = [f"Profile '{profile_id}' prepared."]

    if preview:
        notes.append("Preview only: no persistent changes applied.")
        return ProfileApplyResult(ok=True, profile_id=profile_id, notes=notes)

    for skill_id in profile.skills:
        skill_result = apply_skill(skill_id, preview=False)
        notes.append(f"Applied skill '{skill_id}': ok={skill_result.ok}")

    overrides = load_runtime_overrides()
    merged_overrides = _deep_merge(overrides, profile.config_overrides)
    save_runtime_overrides(merged_overrides)
    notes.append("Runtime overrides updated from profile.")

    model_policy = load_model_selector_policy()
    prefer = model_policy.setdefault("prefer_by_role", {})
    for role, model_id in profile.model_preferences.items():
        prefer[role] = model_id
    save_model_selector_policy(model_policy)
    notes.append("Model preferences updated from profile.")

    router_policy = load_router_policy()
    merged_keywords = set(router_policy.get("retrieve_keywords", []))
    merged_keywords.update([kw.lower() for kw in profile.router_keywords])
    router_policy["retrieve_keywords"] = sorted(merged_keywords)
    save_router_policy(router_policy)
    notes.append("Router policy updated from profile.")

    critic_policy = load_critic_policy()
    critic_policy.update(profile.critic_policy)
    save_critic_policy(critic_policy)
    notes.append("Critic policy updated from profile.")

    return ProfileApplyResult(ok=True, profile_id=profile_id, notes=notes)
