from numax.specs.assumption_map import AssumptionItem, AssumptionMap
from numax.specs.intent_spec import IntentSpec
from numax.specs.validator import validate_spec_bundle
from numax.specs.work_spec import WorkSpec


def test_validate_spec_bundle_ok():
    intent = IntentSpec(
        objective="Fix bug",
        user_request="Fix bug",
        ambiguity_level="low",
    )
    assumptions = AssumptionMap(
        items=[AssumptionItem(statement="x", status="explicit", impact="low")]
    )
    work = WorkSpec(
        title="Bugfix",
        deliverables=["patch"],
        acceptance_criteria=["tests pass"],
        ready=True,
    )

    result = validate_spec_bundle(intent, work, assumptions)
    assert result["ok"] is True
