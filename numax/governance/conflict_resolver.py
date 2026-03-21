from __future__ import annotations

from dataclasses import dataclass
from typing import List

from numax.governance.constitution import NumaxConstitution, build_default_constitution


@dataclass
class GovernanceConflict:
    left: str
    right: str
    context: str = ""


@dataclass
class GovernanceResolution:
    winner: str
    loser: str
    rationale: str


class GovernanceConflictResolver:
    def __init__(self, constitution: NumaxConstitution | None = None) -> None:
        self.constitution = constitution or build_default_constitution()

    def resolve(self, conflict: GovernanceConflict) -> GovernanceResolution:
        left_rule = self.constitution.get(conflict.left)
        right_rule = self.constitution.get(conflict.right)

        if left_rule.priority > right_rule.priority:
            return GovernanceResolution(
                winner=left_rule.name,
                loser=right_rule.name,
                rationale=(
                    f"'{left_rule.name}' wins because it has higher priority "
                    f"({left_rule.priority}) than '{right_rule.name}' ({right_rule.priority})."
                ),
            )

        if right_rule.priority > left_rule.priority:
            return GovernanceResolution(
                winner=right_rule.name,
                loser=left_rule.name,
                rationale=(
                    f"'{right_rule.name}' wins because it has higher priority "
                    f"({right_rule.priority}) than '{left_rule.name}' ({left_rule.priority})."
                ),
            )

        return GovernanceResolution(
            winner=left_rule.name,
            loser=right_rule.name,
            rationale=(
                f"Equal priority conflict between '{left_rule.name}' and '{right_rule.name}'. "
                f"Defaulting to left rule."
            ),
        )

    def resolve_many(self, candidates: List[str]) -> str:
        if not candidates:
            raise ValueError("No candidates provided for conflict resolution.")

        sorted_rules = sorted(
            [self.constitution.get(name) for name in candidates],
            key=lambda rule: rule.priority,
            reverse=True,
        )
        return sorted_rules[0].name
