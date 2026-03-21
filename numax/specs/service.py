from __future__ import annotations

from typing import List

from numax.specs.assumption_map import AssumptionItem, AssumptionMap
from numax.specs.intent_spec import IntentSpec
from numax.specs.work_spec import WorkSpec


class SpecService:
    def build_intent_spec(self, raw_input: str) -> IntentSpec:
        text = raw_input.strip()

        task_type = "general_request"
        domain = "general"
        ambiguity = "medium"

        lowered = text.lower()
        if any(word in lowered for word in ["fix", "repair", "bug", "patch"]):
            task_type = "repo_change"
            domain = "software"
        elif any(word in lowered for word in ["benchmark", "compare", "measure"]):
            task_type = "evaluation"
            domain = "systems"

        if len(text.split()) < 5:
            ambiguity = "high"

        return IntentSpec(
            objective=text,
            user_request=text,
            domain=domain,
            task_type=task_type,
            constraints=[],
            success_definition="Produce a valid, bounded result aligned with the objective.",
            ambiguity_level=ambiguity,
        )

    def build_assumption_map(self, intent_spec: IntentSpec) -> AssumptionMap:
        items: list[AssumptionItem] = [
            AssumptionItem(
                statement="The user wants an actionable result, not only a description.",
                status="inferred",
                impact="medium",
            )
        ]

        if intent_spec.task_type == "repo_change":
            items.append(
                AssumptionItem(
                    statement="The active workspace contains the relevant files.",
                    status="unverified",
                    impact="high",
                )
            )

        return AssumptionMap(items=items)

    def build_work_spec(self, intent_spec: IntentSpec, assumptions: AssumptionMap) -> WorkSpec:
        steps: List[str] = ["Clarify task", "Plan work", "Execute bounded actions", "Validate result"]
        deliverables: List[str] = ["final_output"]
        scope_in: List[str] = [intent_spec.objective]
        scope_out: List[str] = []
        risks: List[str] = []

        if intent_spec.task_type == "repo_change":
            steps = [
                "Inspect workspace",
                "Find target files",
                "Propose patch",
                "Run tests",
                "Review change",
            ]
            deliverables = ["patch_review", "test_result", "recommended_next_action"]
            risks.append("Incorrect file targeting")
            risks.append("Patch may break tests")

        return WorkSpec(
            title=f"Spec for: {intent_spec.objective[:80]}",
            scope_in=scope_in,
            scope_out=scope_out,
            deliverables=deliverables,
            steps=steps,
            risks=risks,
            dependencies=[],
            acceptance_criteria=[
                "Result is bounded",
                "Result is traceable",
                "Result matches requested objective",
            ],
            ready=True,
        )
