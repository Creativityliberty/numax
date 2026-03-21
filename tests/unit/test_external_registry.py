from numax.subagents.external import build_default_external_subagent_registry


def test_external_subagent_registry_has_mock_worker():
    registry = build_default_external_subagent_registry()
    assert "mock_repo_worker" in registry.list_ids()
