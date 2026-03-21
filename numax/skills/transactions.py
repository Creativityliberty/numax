from __future__ import annotations

from dataclasses import dataclass

from numax.skills.effects import apply_effect, capture_effect_previous_state, revert_effect
from numax.skills.specs import InstallableSkill


@dataclass
class SkillTransactionResult:
    ok: bool
    applied_count: int
    reverted_count: int
    previous_states: list[dict]
    notes: list[str]


def apply_skill_transaction(skill: InstallableSkill) -> SkillTransactionResult:
    notes: list[str] = []
    previous_states: list[dict] = []
    applied: list[dict] = []

    try:
        for effect in skill.effects:
            state = capture_effect_previous_state(effect)
            previous_states.append(state)
            result = apply_effect(effect)
            notes.append(f"Applied effect: {result}")
            if not result.get("ok", False):
                raise RuntimeError(f"Effect failed: {result}")
            applied.append(state)

        return SkillTransactionResult(
            ok=True,
            applied_count=len(applied),
            reverted_count=0,
            previous_states=previous_states,
            notes=notes,
        )
    except Exception as exc:
        reverted_count = 0
        for state in reversed(applied):
            revert = revert_effect(state)
            notes.append(f"Reverted after failure: {revert}")
            if revert.get("ok", False):
                reverted_count += 1

        notes.append(f"Transaction failed: {exc}")
        return SkillTransactionResult(
            ok=False,
            applied_count=len(applied),
            reverted_count=reverted_count,
            previous_states=previous_states,
            notes=notes,
        )
