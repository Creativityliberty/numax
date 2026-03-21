from __future__ import annotations

from numax.skills.specs import InstallableSkill, SkillEffect


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, InstallableSkill] = {}

    def register(self, skill: InstallableSkill) -> None:
        self._skills[skill.skill_id] = skill

    def get(self, skill_id: str) -> InstallableSkill:
        if skill_id not in self._skills:
            raise KeyError(f"Unknown skill: {skill_id}")
        return self._skills[skill_id]

    def list_ids(self) -> list[str]:
        return sorted(self._skills.keys())


def build_default_skill_registry() -> SkillRegistry:
    registry = SkillRegistry()

    registry.register(
        InstallableSkill(
            skill_id="memory_plus",
            title="Memory Plus",
            description="Raise memory-related runtime preferences.",
            effects=[
                SkillEffect(
                    effect_type="set_config_value",
                    payload={"path": "runtime.max_retries", "value": 3},
                ),
            ],
        )
    )

    registry.register(
        InstallableSkill(
            skill_id="research_mode",
            title="Research Mode",
            description="Bias router and retrieval toward research-oriented behavior.",
            effects=[
                SkillEffect(
                    effect_type="append_router_keyword",
                    payload={"keyword": "paper"},
                ),
                SkillEffect(
                    effect_type="append_router_keyword",
                    payload={"keyword": "survey"},
                ),
            ],
        )
    )

    registry.register(
        InstallableSkill(
            skill_id="critic_strict",
            title="Critic Strict",
            description="Enable stricter critic calibration.",
            effects=[
                SkillEffect(
                    effect_type="set_critic_policy",
                    payload={"strict_mode": True},
                ),
            ],
        )
    )

    registry.register(
        InstallableSkill(
            skill_id="fast_primary",
            title="Fast Primary",
            description="Prefer lighter model for primary role.",
            effects=[
                SkillEffect(
                    effect_type="set_model_preference",
                    payload={"role": "primary", "model_id": "mock:mock-small"},
                ),
            ],
        )
    )

    return registry
