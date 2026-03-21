from benchmarks.metrics import compare_systems


def test_compare_systems_returns_winner():
    summary = {
        "numax": {
            "task_success_rate": 1.0,
            "artifact_validity_rate": 1.0,
            "recovery_success_rate": 1.0,
            "continuity_resume_score": 0.9,
            "budget_efficiency_score": 0.8,
            "mutation_safety_score": 1.0,
            "count": 6,
        },
        "llm_only": {
            "task_success_rate": 0.8,
            "artifact_validity_rate": 0.0,
            "recovery_success_rate": 0.2,
            "continuity_resume_score": 0.2,
            "budget_efficiency_score": 0.9,
            "mutation_safety_score": 0.0,
            "count": 6,
        },
    }

    result = compare_systems(summary)

    assert result["winner"] == "numax"
    assert "numax" in result["ranking"]
