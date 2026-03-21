from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from numax.skills.effects import apply_effect, capture_effect_previous_state
from numax.skills.journal import append_entry, current_installed_skills, mark_last_known_good
from numax.skills.registry import build_default_skill_registry
from numax.skills.snapshots import save_skill_snapshot


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

    snapshot: dict[str, Any] = {"skill_id": skill_id, "previous_states": []}

    for effect in skill.effects:
        snapshot["previous_states"].append(capture_effect_previous_state(effect))
        result = apply_effect(effect)
        notes.append(f"Applied effect: {result}")

    save_skill_snapshot(skill_id, snapshot)
    append_entry({"action": "apply", "skill_id": skill_id, "version": skill.version})
    mark_last_known_good(current_installed_skills())
    notes.append("Skill apply persisted with reversible snapshot.")

    return SkillApplyResult(ok=True, skill_id=skill_id, preview=False, notes=notes)
