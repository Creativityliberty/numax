from numax.tools.workspace_tools import WorkspaceTools


def test_workspace_tools_git_diff_no_crash(tmp_path):
    tools = WorkspaceTools()
    result = tools.diff(str(tmp_path))

    # Even if not a git repo, it should return a result dict with 'ok'
    assert "ok" in result
