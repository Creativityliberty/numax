from __future__ import annotations

from dataclasses import dataclass

from numax.skills.effects import apply_effect
from numax.skills.journal import append_entry, current_installed_skills, mark_last_known_good
from numax.skills.registry import build_default_skill_registry


@dataclass
class SkillApplyResult:
    ok: bool
    skill_id: str
    preview: bool
    notes: list[str]


def apply_skill(skill_id: str, preview: bool = True) -> SkillApplyResult:
    registry = build_default_skill_registry()
    skill = registry.get(skill_id)

    notes = [f"Skill '{skill_id}' prepared for apply."]

    if preview:
        notes.append("Preview only: no persistent change applied.")
        return SkillApplyResult(ok=True, skill_id=skill_id, preview=True, notes=notes)

    for effect in skill.effects:
        result = apply_effect(effect)
        notes.append(f"Applied effect: {result}")

    append_entry({"action": "apply", "skill_id": skill_id, "version": skill.version})
    mark_last_known_good(current_installed_skills())
    notes.append("Skill apply persisted to local JSON journal and runtime policies.")

    return SkillApplyResult(ok=True, skill_id=skill_id, preview=False, notes=notes)
