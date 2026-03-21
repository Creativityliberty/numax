from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from numax.skills.effects import apply_effect
from numax.skills.journal import current_installed_skills, load_skill_journal
from numax.skills.registry import build_default_skill_registry


@dataclass
class ReplayResult:
    ok: bool
    applied: list[str]
    notes: list[str]


def replay_skills(skill_ids: Iterable[str] | None = None) -> ReplayResult:
    notes: list[str] = []
    registry = build_default_skill_registry()

    if skill_ids is None:
        journal = load_skill_journal()
        applied = current_installed_skills()
        notes.append(f"Replayed from journal with {len(journal.get('entries', []))} entries.")
    else:
        applied = list(skill_ids)
        notes.append("Replayed from explicit skill list.")

    for skill_id in applied:
        skill = registry.get(skill_id)
        for effect in skill.effects:
            result = apply_effect(effect)
            notes.append(f"Replayed effect for {skill_id}: {result}")

    return ReplayResult(ok=True, applied=applied, notes=notes)
