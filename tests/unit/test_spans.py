from numax.obs.spans import SpanManager


def test_span_manager_creates_and_finishes_span() -> None:
    manager = SpanManager()
    trace_id = manager.new_trace_id()
    span = manager.start_span("test", trace_id)
    span.add_event("hello", value=1)
    record = span.finish()

    assert record["name"] == "test"
    assert record["trace_id"] == trace_id
