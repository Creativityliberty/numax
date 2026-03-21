from numax.improve.retry_policy import decide_retry_policy


def test_retry_policy_returns_retry_for_patch_revision():
    result = decide_retry_policy(
        suggestions=[{"type": "revise_patch", "priority": "medium"}],
        retries=0,
        max_retries=3,
    )

    assert result["decision"] == "retry"
