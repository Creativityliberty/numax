from numax.specs.service import SpecService


def test_build_intent_spec():
    service = SpecService()
    spec = service.build_intent_spec("Fix the failing test in the repo")

    assert spec.objective
    assert spec.task_type in {"repo_change", "evaluation", "general_request"}
