from numax.skills.registry import build_default_skill_registry


def test_default_skill_registry_has_known_skills() -> None:
    registry = build_default_skill_registry()
    ids = registry.list_ids()

    assert "memory_plus" in ids
    assert "research_mode" in ids
