from numax.core.state import NumaxState
from numax.flows.workspace_search import build_workspace_search_flow


def test_workspace_search_flow(tmp_path):
    (tmp_path / "README.md").write_text("NUMAX workspace hello", encoding="utf-8")

    state = NumaxState(
        observation={
            "workspace_path": str(tmp_path),
            "search_query": "hello",
        }
    )

    graph = build_workspace_search_flow()
    final_state = graph.run(start="workspace_open", state=state)

    result = final_state.world_state.get("workspace_search", {})
    assert result.get("ok") is True
    assert len(result.get("results", [])) > 0
