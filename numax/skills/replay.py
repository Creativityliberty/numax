from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass
class ReplayResult:
    ok: bool
    applied: list[str]
    notes: list[str]


def replay_skills(skill_ids: Iterable[str]) -> ReplayResult:
    applied: list[str] = []
    notes: list[str] = []

    for skill_id in skill_ids:
        applied.append(skill_id)
        notes.append(f"Replayed skill: {skill_id}")

    return ReplayResult(
        ok=True,
        applied=applied,
        notes=notes,
    )
