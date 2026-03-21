from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SkillUninstallResult:
    ok: bool
    skill_id: str
    notes: list[str]


def uninstall_skill(skill_id: str) -> SkillUninstallResult:
    return SkillUninstallResult(
        ok=True,
        skill_id=skill_id,
        notes=[f"Skill '{skill_id}' uninstall stub executed."],
    )
