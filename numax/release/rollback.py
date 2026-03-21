from __future__ import annotations

from dataclasses import dataclass

from numax.skills.journal import load_skill_journal


@dataclass
class RollbackResult:
    ok: bool
    target: str
    restored_skills: list[str]
    notes: list[str]


def rollback_to(target: str = "last_known_good") -> RollbackResult:
    journal = load_skill_journal()
    restored = list(journal.get("last_known_good", []))

    return RollbackResult(
        ok=True,
        target=target,
        restored_skills=restored,
        notes=[f"Rollback restored last known good set: {restored}"],
    )
