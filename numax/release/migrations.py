from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MigrationResult:
    ok: bool
    from_version: str
    to_version: str
    notes: list[str]


def run_migration(from_version: str, to_version: str) -> MigrationResult:
    return MigrationResult(
        ok=True,
        from_version=from_version,
        to_version=to_version,
        notes=[f"Migration stub from {from_version} to {to_version} executed."],
    )
