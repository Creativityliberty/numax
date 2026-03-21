from numax.runtime.timeout_policy import decide_timeout_policy


def test_timeout_policy_repo_change():
    result = decide_timeout_policy(
        flow_name="repo_repair",
        task_type="repo_change",
        degraded=False,
    )

    assert result["timeout_seconds"] >= 120
