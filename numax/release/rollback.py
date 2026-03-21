from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RollbackResult:
    ok: bool
    target: str
    notes: list[str]


def rollback_to(target: str) -> RollbackResult:
    return RollbackResult(
        ok=True,
        target=target,
        notes=[f"Rollback stub executed to target '{target}'."],
    )
