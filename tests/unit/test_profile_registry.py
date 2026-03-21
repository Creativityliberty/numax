from numax.profiles.registry import build_default_profile_registry


def test_default_profile_registry_has_profiles():
    registry = build_default_profile_registry()
    ids = registry.list_ids()

    assert "repo_operator" in ids
    assert "research_mode" in ids
