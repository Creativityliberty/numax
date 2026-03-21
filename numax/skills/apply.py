from __future__ import annotations

from dataclasses import dataclass

from numax.skills.journal import append_entry, current_installed_skills, mark_last_known_good


@dataclass
class SkillApplyResult:
    ok: bool
    skill_id: str
    preview: bool
    notes: list[str]


def apply_skill(skill_id: str, preview: bool = True) -> SkillApplyResult:
    notes = [f"Skill '{skill_id}' prepared for apply."]

    if preview:
        notes.append("Preview only: no persistent change applied.")
        return SkillApplyResult(ok=True, skill_id=skill_id, preview=True, notes=notes)

    append_entry({"action": "apply", "skill_id": skill_id})
    mark_last_known_good(current_installed_skills())
    notes.append("Skill apply persisted to local JSON journal.")

    return SkillApplyResult(ok=True, skill_id=skill_id, preview=False, notes=notes)
