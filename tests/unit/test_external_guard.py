from numax.guardian.enforcer import enforce_external_subagent


def test_external_guard_allows_admin():
    result = enforce_external_subagent(
        user_roles=["admin"],
        subagent_id="mock_repo_worker",
        mode="full_bounded",
    )

    assert result["ok"] is True
