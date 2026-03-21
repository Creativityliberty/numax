from numax.tools.workspace_tools import WorkspaceTools


def test_workspace_tools_test_runner_no_crash(tmp_path):
    tools = WorkspaceTools()
    result = tools.test(str(tmp_path), command=["echo", "ok"])

    assert result["ok"] is True
