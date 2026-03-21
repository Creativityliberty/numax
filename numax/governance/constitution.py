from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from numax.governance.priorities import GovernancePriority


@dataclass
class ConstitutionalRule:
    name: str
    description: str
    priority: GovernancePriority
    blocking: bool = False


@dataclass
class NumaxConstitution:
    rules: Dict[str, ConstitutionalRule] = field(default_factory=dict)

    def get(self, name: str) -> ConstitutionalRule:
        if name not in self.rules:
            raise KeyError(f"Unknown constitutional rule: {name}")
        return self.rules[name]

    def list_rules(self) -> List[ConstitutionalRule]:
        return sorted(
            self.rules.values(),
            key=lambda rule: rule.priority,
            reverse=True,
        )


def build_default_constitution() -> NumaxConstitution:
    rules = {
        "safety_first": ConstitutionalRule(
            name="safety_first",
            description="Safety constraints override all other concerns.",
            priority=GovernancePriority.SAFETY,
            blocking=True,
        ),
        "governance_integrity": ConstitutionalRule(
            name="governance_integrity",
            description="Invariants, versioning and policy constraints must be preserved.",
            priority=GovernancePriority.GOVERNANCE,
            blocking=True,
        ),
        "serve_user_goal": ConstitutionalRule(
            name="serve_user_goal",
            description="The system should remain faithful to the validated user goal.",
            priority=GovernancePriority.USER_FIDELITY,
            blocking=False,
        ),
        "preserve_output_quality": ConstitutionalRule(
            name="preserve_output_quality",
            description="Prefer higher-quality outputs if safety and governance allow it.",
            priority=GovernancePriority.QUALITY,
            blocking=False,
        ),
        "preserve_continuity": ConstitutionalRule(
            name="preserve_continuity",
            description="Prefer continuity when it does not conflict with higher-order rules.",
            priority=GovernancePriority.CONTINUITY,
            blocking=False,
        ),
        "control_cost": ConstitutionalRule(
            name="control_cost",
            description="Avoid unnecessary compute and tool spending.",
            priority=GovernancePriority.COST,
            blocking=False,
        ),
        "prefer_speed_when_safe": ConstitutionalRule(
            name="prefer_speed_when_safe",
            description="Prefer faster execution when it does not degrade critical objectives.",
            priority=GovernancePriority.SPEED,
            blocking=False,
        ),
    }
    return NumaxConstitution(rules=rules)
