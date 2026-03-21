from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.specs.service import SpecService
from numax.specs.validator import validate_spec_bundle


class IntentSpecNode(NumaxNode):
    name = "intent_spec"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "raw_input": state.observation.get("raw_input", ""),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        service = SpecService()
        intent_spec = service.build_intent_spec(payload["raw_input"])
        assumptions = service.build_assumption_map(intent_spec)
        work_spec = service.build_work_spec(intent_spec, assumptions)

        return {
            "intent_spec": intent_spec.model_dump(),
            "assumptions": assumptions.model_dump(),
            "work_spec": work_spec.model_dump(),
        }

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.intent_spec = result["intent_spec"]
        state.assumptions = result["assumptions"]
        state.work_spec = result["work_spec"]
        state.acceptance_criteria = result["work_spec"].get("acceptance_criteria", [])
        state.spec_status = "drafted"
        state.add_trace(self.name, "post", "Spec bundle drafted")
        return "validate"


class SpecValidationNode(NumaxNode):
    name = "spec_validation"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "intent_spec": state.intent_spec,
            "assumptions": state.assumptions,
            "work_spec": state.work_spec,
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        from numax.specs.assumption_map import AssumptionMap
        from numax.specs.intent_spec import IntentSpec
        from numax.specs.work_spec import WorkSpec

        result = validate_spec_bundle(
            intent_spec=IntentSpec(**payload["intent_spec"]),
            work_spec=WorkSpec(**payload["work_spec"]),
            assumption_map=AssumptionMap(**payload["assumptions"]),
        )
        return {"validation": result}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        validation = result["validation"]
        state.world_state["spec_validation"] = validation
        state.spec_status = "validated" if validation["ok"] else "needs_clarification"
        state.next_recommended_action = (
            "proceed_to_execution" if validation["ok"] else "clarify_spec"
        )
        state.add_trace(
            self.name,
            "post",
            "Spec validation completed",
            ok=validation["ok"],
            confidence=validation["confidence"],
        )
        return "done"
