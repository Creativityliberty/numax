from numax.tools.patch_apply import apply_text_patch


def test_apply_text_patch_real(tmp_path):
    target = tmp_path / "a.py"
    target.write_text("print('hello')\n", encoding="utf-8")

    result = apply_text_patch(
        path=str(target),
        old_text="print('hello')",
        new_text="print('world')",
        preview_only=False,
    )

    assert result["ok"] is True
    assert "world" in target.read_text(encoding="utf-8")
