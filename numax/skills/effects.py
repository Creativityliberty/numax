from __future__ import annotations

from numax.learning.critic_calibration import load_critic_policy, save_critic_policy
from numax.learning.model_selector import load_model_selector_policy, save_model_selector_policy
from numax.learning.router import load_router_policy, save_router_policy
from numax.skills.runtime_overrides import (
    load_runtime_overrides,
    save_runtime_overrides,
    set_nested_value,
)
from numax.skills.specs import SkillEffect


def apply_effect(effect: SkillEffect) -> dict:
    if effect.effect_type == "set_config_value":
        overrides = load_runtime_overrides()
        set_nested_value(overrides, str(effect.payload.get("path")), effect.payload.get("value"))
        save_runtime_overrides(overrides)
        return {"effect": effect.effect_type, "ok": True}

    if effect.effect_type == "append_router_keyword":
        policy = load_router_policy()
        merged = set(policy.get("retrieve_keywords", []))
        merged.add(str(effect.payload.get("keyword")).lower())
        policy["retrieve_keywords"] = sorted(list(merged))
        save_router_policy(policy)
        return {"effect": effect.effect_type, "ok": True}

    if effect.effect_type == "set_model_preference":
        policy = load_model_selector_policy()
        prefer = policy.setdefault("prefer_by_role", {})
        prefer[str(effect.payload.get("role"))] = str(effect.payload.get("model_id"))
        save_model_selector_policy(policy)
        return {"effect": effect.effect_type, "ok": True}

    if effect.effect_type == "set_critic_policy":
        policy = load_critic_policy()
        for key, value in effect.payload.items():
            policy[key] = value
        save_critic_policy(policy)
        return {"effect": effect.effect_type, "ok": True}

    return {"effect": effect.effect_type, "ok": False, "reason": "unknown_effect_type"}
