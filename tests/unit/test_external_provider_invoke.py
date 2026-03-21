from numax.subagents.contracts import ExternalSubagentRequest
from numax.subagents.external import build_default_external_subagent_registry


def test_external_provider_invoke():
    registry = build_default_external_subagent_registry()
    provider = registry.get("mock_repo_worker")

    response = provider.invoke(
        ExternalSubagentRequest(
            task="Inspect repo",
            mode="read_only",
            active_files=["main.py"],
        )
    )

    assert response.ok is True
    assert response.subagent_id == "mock_repo_worker"
