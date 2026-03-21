from numax.critic.code_critic import review_code_change


def test_code_critic_accept():
    review = review_code_change(
        patch={
            "path": "app/main.py",
            "apply_result": {
                "ok": True,
                "preview_only": False,
                "before_excerpt": "print('a')",
                "after_excerpt": "print('b')",
            },
        },
        test_result={"ok": True},
        active_files=["app/main.py"],
    )

    assert review["decision"] == "accept"
    assert review["risk"] == "low"
