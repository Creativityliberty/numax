from __future__ import annotations

import uuid
from typing import Any

from numax.configs.loader import get_budget_limits, get_runtime_autonomy_mode, load_config
from numax.core.state import NumaxState
from numax.flows.artifact_output import build_artifact_output_flow
from numax.flows.basic_chat import build_basic_chat_flow
from numax.flows.planning_execution import build_planning_execution_flow
from numax.flows.retrieval_answer import build_retrieval_answer_flow
from numax.obs.runtime_hooks import instrument_flow_end, instrument_flow_start
from numax.obs.spans import SpanManager

SPAN_MANAGER = SpanManager()


def _build_flow(flow_name: str) -> Any:
    if flow_name == "basic_chat":
        return build_basic_chat_flow()
    if flow_name == "retrieval_answer":
        return build_retrieval_answer_flow()
    if flow_name == "planning_execution":
        return build_planning_execution_flow()
    if flow_name == "artifact_output":
        return build_artifact_output_flow()
    raise ValueError(f"Unsupported flow: {flow_name}")


def run_job_flow(flow: str, prompt: str, metadata: dict | None = None) -> dict:
    config = load_config()
    budget_cfg = get_budget_limits(config)

    state = NumaxState(observation={"raw_input": prompt})
    state.runtime.run_id = str(uuid.uuid4())
    state.budget.max_tokens_total = budget_cfg["max_tokens_total"]
    state.budget.max_cost_usd = budget_cfg["max_cost_usd"]
    state.world_state["autonomy_mode"] = get_runtime_autonomy_mode(config)
    state.world_state["artifact_type"] = "summary"
    state.world_state["artifact_title"] = "Job Artifact"
    if metadata:
        state.world_state["job_metadata"] = metadata

    trace_id = SPAN_MANAGER.new_trace_id()
    start_span = instrument_flow_start(flow, trace_id, run_id=state.runtime.run_id)

    try:
        graph = _build_flow(flow)
        final_state = graph.run(start="intent_router", state=state)
        start_span.add_event("flow_result", fsm_state=final_state.runtime.fsm_state)
        start_span.finish()
        instrument_flow_end(flow, trace_id, ok=True, run_id=state.runtime.run_id)
        return {
            "ok": True,
            "run_id": final_state.runtime.run_id,
            "final_output": final_state.final_output,
            "artifact": final_state.world_state.get("artifact"),
            "trace_count": len(final_state.trace),
            "fsm_state": final_state.runtime.fsm_state,
        }
    except Exception as exc:
        start_span.set_status("error")
        start_span.add_event("flow_error", error=str(exc))
        start_span.finish()
        instrument_flow_end(flow, trace_id, ok=False, run_id=state.runtime.run_id)
        return {
            "ok": False,
            "error": str(exc),
        }
