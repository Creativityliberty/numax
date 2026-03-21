from numax.tools.workspace_tools import WorkspaceTools


def test_workspace_tools_search(tmp_path):
    (tmp_path / "a.py").write_text("def hello():\n    return 1\n", encoding="utf-8")
    (tmp_path / "b.md").write_text("hello world", encoding="utf-8")

    tools = WorkspaceTools()
    result = tools.search(str(tmp_path), "hello")

    assert result["ok"] is True
    assert len(result["results"]) >= 2
