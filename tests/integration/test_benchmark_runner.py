from benchmarks.runner import run_benchmarks


def test_run_benchmarks_returns_summary():
    report = run_benchmarks()

    assert "results" in report
    assert "summary" in report
    assert "numax" in report["summary"]
