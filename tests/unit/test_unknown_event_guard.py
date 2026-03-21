from numax.runtime.unknown_event_guard import guard_event


def test_guard_unknown_event():
    event = {"kind": "strange_sdk_event", "name": "weird", "payload": {"x": 1}}
    result = guard_event(event)

    assert result["kind"] == "unknown"
    assert result["guarded"] is True
