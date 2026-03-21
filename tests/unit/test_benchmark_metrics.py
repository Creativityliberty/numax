from benchmarks.metrics import summarize_metrics


def test_summarize_metrics_has_expected_keys():
    rows = [
        {
            "task_success": True,
            "artifact_valid": True,
            "recovered": True,
            "continuity_score": 0.8,
            "cost_used_usd": 0.05,
            "tokens_used": 1000,
            "rollback_ok": False,
            "replay_ok": False,
        }
    ]

    summary = summarize_metrics(rows)

    assert "task_success_rate" in summary
    assert "artifact_validity_rate" in summary
    assert "budget_efficiency_score" in summary
