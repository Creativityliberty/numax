from numax.learning.mode_feedback import append_mode_feedback
from numax.learning.mode_selector import select_best_mode


def test_select_best_mode():
    append_mode_feedback(
        {
            "profile": "research_mode",
            "recipe": None,
            "success": True,
            "rollback": False,
            "duration_seconds": 1.0,
            "cost_used_usd": 0.0,
            "retries": 0,
            "quality_score": 0.95,
        }
    )

    result = select_best_mode(group_by="profile", min_runs=1)
    assert "selected" in result
