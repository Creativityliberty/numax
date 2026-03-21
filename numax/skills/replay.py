from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from numax.skills.journal import current_installed_skills, load_skill_journal


@dataclass
class ReplayResult:
    ok: bool
    applied: list[str]
    notes: list[str]


def replay_skills(skill_ids: Iterable[str] | None = None) -> ReplayResult:
    notes: list[str] = []

    if skill_ids is None:
        journal = load_skill_journal()
        applied = current_installed_skills()
        notes.append(f"Replayed from journal with {len(journal.get('entries', []))} entries.")
    else:
        applied = list(skill_ids)
        notes.append("Replayed from explicit skill list.")

    for skill_id in applied:
        notes.append(f"Replayed skill: {skill_id}")

    return ReplayResult(ok=True, applied=applied, notes=notes)
