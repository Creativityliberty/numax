from numax.workspace.service import WorkspaceService


def test_open_workspace(tmp_path):
    service = WorkspaceService()
    ctx = service.open_workspace(str(tmp_path))

    assert ctx.root_path
    assert ctx.workspace_id
