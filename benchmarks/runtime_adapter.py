from __future__ import annotations

import uuid
from typing import Any

from numax.configs.loader import (
    get_budget_limits,
    get_runtime_autonomy_mode,
    load_config,
)
from numax.core.state import NumaxState
from numax.flows.artifact_output import build_artifact_output_flow
from numax.flows.basic_chat import build_basic_chat_flow
from numax.flows.planning_execution import build_planning_execution_flow
from numax.flows.retrieval_answer import build_retrieval_answer_flow


def _build_flow(flow_name: str):
    if flow_name == "basic_chat":
        return build_basic_chat_flow()
    if flow_name == "retrieval_answer":
        return build_retrieval_answer_flow()
    if flow_name == "planning_execution":
        return build_planning_execution_flow()
    if flow_name == "artifact_output":
        return build_artifact_output_flow()
    raise ValueError(f"Unsupported benchmark flow: {flow_name}")


def run_numax_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    config = load_config()
    budget_cfg = get_budget_limits(config)

    state = NumaxState(
        observation={"raw_input": scenario["prompt"]},
    )
    state.runtime.run_id = str(uuid.uuid4())
    state.budget.max_tokens_total = scenario.get(
        "max_tokens_total",
        budget_cfg["max_tokens_total"],
    )
    state.budget.max_cost_usd = scenario.get(
        "max_cost_usd",
        budget_cfg["max_cost_usd"],
    )
    state.world_state["autonomy_mode"] = get_runtime_autonomy_mode(config)
    state.world_state["artifact_type"] = scenario.get("artifact_type", "summary")
    state.world_state["artifact_title"] = scenario.get("artifact_title", "Benchmark Artifact")

    if scenario.get("inject_retrieved_context"):
        state.retrieved_context = scenario["inject_retrieved_context"]
        state.confidence.source_confidence = 0.8

    graph = _build_flow(scenario["flow"])
    final_state = graph.run(start="intent_router", state=state)

    artifact = final_state.world_state.get("artifact")
    artifact_valid = False
    if artifact:
        artifact_valid = artifact.get("status") == "validated"

    continuity_score = 1.0 if final_state.memory.get("continuity") else 0.4

    return {
        "scenario_id": scenario["scenario_id"],
        "system": "numax",
        "flow": scenario["flow"],
        "task_success": final_state.final_output is not None,
        "artifact_valid": artifact_valid,
        "recovered": not final_state.runtime.degraded,
        "continuity_score": continuity_score,
        "cost_used_usd": final_state.budget.cost_used_usd,
        "tokens_used": final_state.budget.tokens_used,
        "rollback_ok": False,
        "replay_ok": False,
        "trace_count": len(final_state.trace),
        "fsm_state": final_state.runtime.fsm_state,
        "has_plan": final_state.plan is not None,
        "final_output": final_state.final_output,
        "artifact": artifact,
    }
