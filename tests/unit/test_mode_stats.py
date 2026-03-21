from numax.learning.mode_feedback import append_mode_feedback
from numax.learning.mode_stats import compute_mode_stats


def test_compute_mode_stats():
    append_mode_feedback(
        {
            "profile": "repo_operator",
            "recipe": "repo_repair_basic",
            "success": True,
            "rollback": False,
            "duration_seconds": 2.0,
            "cost_used_usd": 0.1,
            "retries": 1,
            "quality_score": 0.9,
        }
    )

    result = compute_mode_stats(group_by="profile")
    assert "stats" in result
