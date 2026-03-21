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


def capture_effect_previous_state(effect: SkillEffect) -> dict:
    if effect.effect_type == "set_config_value":
        overrides = load_runtime_overrides()
        path = str(effect.payload.get("path", ""))
        parts = path.split(".")
        cursor = overrides
        for part in parts[:-1]:
            if isinstance(cursor, dict):
                cursor = cursor.get(part, {})
        old_value = cursor.get(parts[-1]) if isinstance(cursor, dict) else None
        return {"effect_type": effect.effect_type, "path": path, "old_value": old_value}

    if effect.effect_type == "append_router_keyword":
        return {
            "effect_type": effect.effect_type,
            "keyword": str(effect.payload.get("keyword")).lower(),
        }

    if effect.effect_type == "set_model_preference":
        policy = load_model_selector_policy()
        role = str(effect.payload.get("role"))
        old_value = policy.get("prefer_by_role", {}).get(role)
        return {"effect_type": effect.effect_type, "role": role, "old_value": old_value}

    if effect.effect_type == "set_critic_policy":
        policy = load_critic_policy()
        old_values = {key: policy.get(key) for key in effect.payload.keys()}
        return {"effect_type": effect.effect_type, "old_values": old_values}

    return {"effect_type": effect.effect_type}


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


def revert_effect(previous_state: dict) -> dict:
    effect_type = previous_state.get("effect_type")

    if effect_type == "set_config_value":
        overrides = load_runtime_overrides()
        set_nested_value(
            overrides, str(previous_state.get("path")), previous_state.get("old_value")
        )
        save_runtime_overrides(overrides)
        return {"effect": effect_type, "ok": True, "reverted": True}

    if effect_type == "append_router_keyword":
        policy = load_router_policy()
        keyword = previous_state.get("keyword")
        values = [x for x in policy.get("retrieve_keywords", []) if x != keyword]
        policy["retrieve_keywords"] = values
        save_router_policy(policy)
        return {"effect": effect_type, "ok": True, "reverted": True}

    if effect_type == "set_model_preference":
        policy = load_model_selector_policy()
        prefer = policy.setdefault("prefer_by_role", {})
        role = str(previous_state.get("role"))
        old_value = previous_state.get("old_value")
        if old_value is None:
            prefer.pop(role, None)
        else:
            prefer[role] = old_value
        save_model_selector_policy(policy)
        return {"effect": effect_type, "ok": True, "reverted": True}

    if effect_type == "set_critic_policy":
        policy = load_critic_policy()
        for key, value in previous_state.get("old_values", {}).items():
            policy[key] = value
        save_critic_policy(policy)
        return {"effect": effect_type, "ok": True, "reverted": True}

    return {"effect": effect_type, "ok": False, "reason": "unknown_effect_type"}
