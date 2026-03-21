from numax.critic.code_critic import review_code_change


def test_code_critic_revise_when_no_tests():
    review = review_code_change(
        patch={
            "path": "app/main.py",
            "apply_result": {
                "ok": True,
                "preview_only": True,
                "before_excerpt": "print('a')",
                "after_excerpt": "print('b')",
            },
        },
        test_result={},
        active_files=["app/main.py"],
    )

    assert review["decision"] == "revise"
