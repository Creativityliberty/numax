from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

SkillEffectType = Literal[
    "set_config_value",
    "append_router_keyword",
    "set_model_preference",
    "set_critic_policy",
]


class SkillEffect(BaseModel):
    effect_type: SkillEffectType
    payload: dict[str, Any] = Field(default_factory=dict)


class InstallableSkill(BaseModel):
    skill_id: str
    title: str
    description: str = ""
    version: str = "0.1.0"
    effects: list[SkillEffect] = Field(default_factory=list)
