from __future__ import annotations

from dataclasses import dataclass

from numax.skills.journal import append_entry, current_installed_skills, mark_last_known_good


@dataclass
class SkillUninstallResult:
    ok: bool
    skill_id: str
    notes: list[str]


def uninstall_skill(skill_id: str) -> SkillUninstallResult:
    append_entry({"action": "uninstall", "skill_id": skill_id})
    mark_last_known_good(current_installed_skills())
    return SkillUninstallResult(
        ok=True,
        skill_id=skill_id,
        notes=[
            f"Skill '{skill_id}' uninstall persisted to local JSON journal.",
            "Note: uninstall currently updates journal state; "
            "effect reversal policy may be added later.",
        ],
    )
