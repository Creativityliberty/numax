from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from numax.skills.journal import current_installed_skills, load_skill_journal
from numax.skills.registry import build_default_skill_registry
from numax.skills.transactions import apply_skill_transaction


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

    all_ok = True
    for skill_id in applied:
        skill = registry.get(skill_id)
        tx = apply_skill_transaction(skill)
        notes.extend(tx.notes)
        if tx.ok:
            notes.append(f"Replayed skill transactionally: {skill_id}")
        else:
            all_ok = False
            notes.append(f"Replay failed for skill: {skill_id}")

    return ReplayResult(ok=all_ok, applied=applied, notes=notes)
