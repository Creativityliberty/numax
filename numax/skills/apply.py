from __future__ import annotations

from dataclasses import dataclass


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
    else:
        notes.append("Skill apply stub executed.")

    return SkillApplyResult(
        ok=True,
        skill_id=skill_id,
        preview=preview,
        notes=notes,
    )
