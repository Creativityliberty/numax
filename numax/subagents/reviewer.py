from __future__ import annotations

from typing import Any, Dict

from numax.core.state import NumaxState
from numax.subagents.base import BaseSubagent


class ReviewerSubagent(BaseSubagent):
    name = "reviewer_subagent"
    role = "reviewer"

    def act(self, state: NumaxState) -> Dict[str, Any]:
        review = state.world_state.get("code_review", {})
        notes = []

        if not review:
            notes.append("No code review found.")
            recommendation = "review_missing"
            severity = "medium"
        else:
            decision = review.get("decision", "revise")
            risk = review.get("risk", "medium")
            scope = review.get("scope", "medium")
            recommendation = decision
            severity = "low"

            if risk == "high":
                severity = "high"
            elif risk == "medium":
                severity = "medium"

            notes.extend(review.get("notes", []))
            notes.append(f"Risk={risk}, Scope={scope}, Decision={decision}")

        return {
            "subagent": self.name,
            "role": self.role,
            "recommendation": recommendation,
            "severity": severity,
            "notes": notes,
        }
