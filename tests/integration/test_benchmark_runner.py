from benchmarks.runner import run_benchmarks


def test_run_benchmarks_returns_summary():
    report = run_benchmarks()

    assert "results" in report
    assert "summary" in report
    assert "numax" in report["summary"]


def test_run_benchmarks_contains_mutation_and_continuity_fields():
    report = run_benchmarks()

    assert report["results"]
    sample = report["results"][0]
    assert "continuity_score" in sample
    assert "rollback_ok" in sample
    assert "replay_ok" in sample
