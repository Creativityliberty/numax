from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SelfChangeDecision:
    allowed: bool
    mode: str
    reason: str


def can_self_change(mutation_mode: str) -> SelfChangeDecision:
    if mutation_mode == "MUTATION_FORBIDDEN":
        return SelfChangeDecision(
            allowed=False,
            mode=mutation_mode,
            reason="Self-change forbidden by governance.",
        )

    if mutation_mode == "MUTATION_PREVIEW_ONLY":
        return SelfChangeDecision(
            allowed=True,
            mode=mutation_mode,
            reason="Preview-only self-change allowed.",
        )

    if mutation_mode == "MUTATION_APPROVED":
        return SelfChangeDecision(
            allowed=True,
            mode=mutation_mode,
            reason="Approved self-change allowed.",
        )

    return SelfChangeDecision(
        allowed=False,
        mode=mutation_mode,
        reason="Unknown mutation mode.",
    )
