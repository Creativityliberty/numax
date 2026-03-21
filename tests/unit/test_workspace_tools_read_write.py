from numax.tools.workspace_tools import WorkspaceTools


def test_workspace_tools_read_write(tmp_path):
    tools = WorkspaceTools()
    target = tmp_path / "hello.txt"

    write_result = tools.write(str(target), "hello", overwrite=True)
    assert write_result["ok"] is True

    read_result = tools.read(str(target))
    assert read_result["ok"] is True
    assert read_result["content"] == "hello"
