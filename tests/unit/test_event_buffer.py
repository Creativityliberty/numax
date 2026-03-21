from numax.runtime.event_buffer import buffer_events
from numax.runtime.events import RuntimeEvent


def test_event_buffer_truncates():
    events = [
        RuntimeEvent(kind="trace", name=f"e{i}")
        for i in range(60)
    ]
    result = buffer_events(events, max_events=10)

    assert result["truncated"] is True
    assert result["kept"] == 10
    assert result["dropped"] == 50
