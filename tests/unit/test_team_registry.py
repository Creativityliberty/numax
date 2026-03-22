from numax.teams.registry import build_default_team_registry


def test_team_registry_has_core_squads():
    registry = build_default_team_registry()
    ids = registry.list_ids()

    assert "product_squad" in ids
    assert "engineering_squad" in ids
    assert "qa_squad" in ids
