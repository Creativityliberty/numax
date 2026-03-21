from __future__ import annotations

from dataclasses import dataclass

from numax.skills.effects import revert_effect
from numax.skills.journal import append_entry, current_installed_skills, mark_last_known_good
from numax.skills.snapshots import delete_skill_snapshot, load_skill_snapshot


@dataclass
class SkillUninstallResult:
    ok: bool
    skill_id: str
    notes: list[str]


def uninstall_skill(skill_id: str) -> SkillUninstallResult:
    notes: list[str] = []
    snapshot = load_skill_snapshot(skill_id)

    for previous_state in reversed(snapshot.get("previous_states", [])):
        result = revert_effect(previous_state)
        notes.append(f"Reverted effect: {result}")

    append_entry({"action": "uninstall", "skill_id": skill_id})
    mark_last_known_good(current_installed_skills())
    delete_skill_snapshot(skill_id)

    notes.append(f"Skill '{skill_id}' uninstall persisted and reverted from snapshot.")
    return SkillUninstallResult(ok=True, skill_id=skill_id, notes=notes)
