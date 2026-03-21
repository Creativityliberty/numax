from numax.skills.registry import build_default_skill_registry
from numax.skills.transactions import apply_skill_transaction


def test_apply_skill_transaction_success() -> None:
    registry = build_default_skill_registry()
    skill = registry.get("memory_plus")

    result = apply_skill_transaction(skill)
    assert result.applied_count >= 1
