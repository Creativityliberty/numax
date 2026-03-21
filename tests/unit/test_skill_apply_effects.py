from numax.skills.apply import apply_skill


def test_apply_skill_preview_succeeds() -> None:
    result = apply_skill("research_mode", preview=True)

    assert result.ok is True
    assert result.preview is True
