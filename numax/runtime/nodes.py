from __future__ import annotations

from typing import Any, Dict, List

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.runtime.event_buffer import buffer_events
from numax.runtime.events import RuntimeEvent
from numax.runtime.timeout_policy import decide_timeout_policy
from numax.runtime.unknown_event_guard import guard_event


class RuntimeCollectEventsNode(NumaxNode):
    name = "runtime_collect_events"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        raw_events = state.world_state.get("runtime_events", [])
        return {"raw_events": raw_events}

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        guarded_events: List[RuntimeEvent] = []

        for item in payload["raw_events"]:
            guarded = guard_event(item)
            guarded_events.append(RuntimeEvent(**guarded))

        return {"events": guarded_events}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.runtime_events = [event.model_dump() for event in result["events"]]
        state.add_trace(self.name, "post", "Runtime events collected", count=len(state.runtime_events))
        return "buffer"


class RuntimeBufferEventsNode(NumaxNode):
    name = "runtime_buffer_events"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {"events": state.runtime_events}

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        events = [RuntimeEvent(**item) for item in payload["events"]]
        buffered = buffer_events(events, max_events=50)
        return {"buffered": buffered}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.event_buffer_status = result["buffered"]
        state.add_trace(
            self.name,
            "post",
            "Runtime events buffered",
            kept=result["buffered"]["kept"],
            dropped=result["buffered"]["dropped"],
            truncated=result["buffered"]["truncated"],
        )
        return "timeout"


class RuntimeTimeoutPolicyNode(NumaxNode):
    name = "runtime_timeout_policy"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "flow_name": state.runtime.flow_name,
            "task_type": state.intent_spec.get("task_type") if state.intent_spec else None,
            "degraded": state.runtime.degraded,
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        decision = decide_timeout_policy(
            flow_name=payload["flow_name"],
            task_type=payload["task_type"],
            degraded=payload["degraded"],
        )
        return {"timeout_decision": decision}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.timeout_decision = result["timeout_decision"]
        state.runtime_resilience_status = "ready"
        state.next_recommended_action = "proceed_with_runtime_policy"
        state.add_trace(
            self.name,
            "post",
            "Timeout policy decided",
            decision=result["timeout_decision"],
        )
        return "done"
