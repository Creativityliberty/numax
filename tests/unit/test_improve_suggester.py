from numax.improve.suggester import suggest_improvements


def test_suggester_detects_test_failure():
    result = suggest_improvements(
        {
            "last_test_run": {"ok": False},
            "code_review": {},
            "spec_validation": {},
            "last_failure": {"kind": "test_failure"},
            "next_recommended_action": "inspect_test_failure",
        }
    )

    types = {item["type"] for item in result["suggestions"]}
    assert "repair_after_test_failure" in types
