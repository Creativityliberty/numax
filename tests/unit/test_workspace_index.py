from numax.workspace.service import WorkspaceService


def test_build_file_index(tmp_path):
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    (tmp_path / "main.py").write_text("print('ok')", encoding="utf-8")

    service = WorkspaceService()
    index = service.build_file_index(str(tmp_path))

    assert len(index.files) >= 2
