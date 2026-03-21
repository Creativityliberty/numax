from numax.rbac.checks import has_permission


def test_admin_has_sandbox_exec() -> None:
    assert has_permission(["admin"], "sandbox.exec") is True


def test_viewer_cannot_run_jobs() -> None:
    assert has_permission(["viewer"], "jobs.run") is False
