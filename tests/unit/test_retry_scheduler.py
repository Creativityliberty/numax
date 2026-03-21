from numax.jobs.retry_scheduler import schedule_retry


def test_schedule_retry_allows_when_under_budget():
    result = schedule_retry("job-1", retries=1, max_retries=3)
    assert result["ok"] is True
