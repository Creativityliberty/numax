from __future__ import annotations

from dataclasses import dataclass

from numax.skills.journal import append_entry, current_installed_skills, mark_last_known_good
from numax.skills.registry import build_default_skill_registry
from numax.skills.snapshots import save_skill_snapshot
from numax.skills.transactions import apply_skill_transaction


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

    tx = apply_skill_transaction(skill)
    notes.extend(tx.notes)

    if not tx.ok:
        return SkillApplyResult(ok=False, skill_id=skill_id, preview=False, notes=notes)

    save_skill_snapshot(skill_id, {"skill_id": skill_id, "previous_states": tx.previous_states})
    append_entry({"action": "apply", "skill_id": skill_id, "version": skill.version})
    mark_last_known_good(current_installed_skills())
    notes.append("Skill apply committed transactionally.")

    return SkillApplyResult(ok=True, skill_id=skill_id, preview=False, notes=notes)
