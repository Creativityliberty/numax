from numax.core.state import NumaxState
from numax.flows.runtime_resilience import build_runtime_resilience_flow


def test_runtime_resilience_flow_runs():
    state = NumaxState()
    state.runtime.flow_name = "repo_repair"
    state.world_state["runtime_events"] = [
        {"kind": "trace", "name": "started", "payload": {}, "severity": "info"},
        {"kind": "strange_unknown", "name": "x", "payload": {}, "severity": "warning"},
    ]

    graph = build_runtime_resilience_flow()
    final_state = graph.run(start="runtime_collect_events", state=state)

    assert final_state.event_buffer_status
    assert final_state.timeout_decision
    assert final_state.runtime_resilience_status == "ready"
