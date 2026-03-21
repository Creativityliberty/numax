from numax.critic.code_critic import review_code_change


def test_code_critic_revert_on_failed_tests():
    review = review_code_change(
        patch={
            "path": "numax/core/state.py",
            "apply_result": {
                "ok": True,
                "preview_only": False,
                "before_excerpt": "x",
                "after_excerpt": "y",
            },
        },
        test_result={"ok": False},
        active_files=["numax/core/state.py"],
    )

    assert review["decision"] == "revert"
    assert review["risk"] == "high"
