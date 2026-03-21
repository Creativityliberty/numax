from numax.profiles.apply import apply_profile


def test_apply_profile_preview():
    result = apply_profile("safe_demo_mode", preview=True)

    assert result.ok is True
    assert result.profile_id == "safe_demo_mode"
