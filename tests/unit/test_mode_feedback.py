from numax.learning.mode_feedback import append_mode_feedback, load_mode_feedback


def test_mode_feedback_append_and_load():
    append_mode_feedback(
        {
            "profile": "safe_demo_mode",
            "recipe": None,
            "success": True,
            "rollback": False,
            "duration_seconds": 1.2,
            "cost_used_usd": 0.0,
            "retries": 0,
            "quality_score": 0.8,
        }
    )

    payload = load_mode_feedback()
    assert "records" in payload
    assert len(payload["records"]) >= 1
