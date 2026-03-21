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
from numax.memory.consolidation import consolidate_patterns
from numax.memory.forgetting import forget_low_value_items
from numax.memory.policy_update import update_memory_policy_from_history
from numax.memory.promotion import (
    promote_episodic_to_semantic,
    promote_working_to_episodic,
)
from numax.memory.retention import trim_memory
from numax.release.rollback import rollback_to
from numax.skills.replay import replay_skills


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


def _simulate_provider_failure(state: NumaxState, scenario: dict[str, Any]) -> None:
    if not scenario.get("provider_failure"):
        return

    state.world_state["forced_provider_failure"] = True
    state.runtime.degraded = True
    state.runtime.fsm_state = "DEGRADED"
    state.add_trace(
        "benchmark",
        "error",
        "Simulated provider failure injected",
        scenario_id=scenario["scenario_id"],
    )


def _apply_memory_pipeline(state: NumaxState) -> dict[str, Any]:
    promoted_episodic = promote_working_to_episodic(state)
    _ = promote_episodic_to_semantic(state.memory)
    state.memory = consolidate_patterns(state.memory)
    state.memory = forget_low_value_items(state.memory)
    state.memory = trim_memory(state.memory)
    policy = update_memory_policy_from_history(state.memory)

    continuity_score = 1.0 if promoted_episodic else 0.5
    if state.memory.get("semantic"):
        continuity_score = min(1.0, continuity_score + 0.2)

    return {
        "continuity_score": continuity_score,
        "promoted_episodic_count": len(promoted_episodic),
        "semantic_count": len(state.memory.get("semantic", [])),
        "memory_policy": policy,
    }


def _apply_mutation_pipeline(scenario: dict[str, Any]) -> dict[str, Any]:
    rollback_ok = False
    replay_ok = False
    notes = []

    if scenario.get("mutation_scenario"):
        replay_result = replay_skills(["core_memory", "governance_guard"])
        replay_ok = replay_result.ok
        notes.extend(replay_result.notes)

        rollback_result = rollback_to("last_known_good")
        rollback_ok = rollback_result.ok
        notes.extend(rollback_result.notes)

    return {
        "rollback_ok": rollback_ok,
        "replay_ok": replay_ok,
        "mutation_notes": notes,
    }


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

    if scenario.get("inject_tool_history"):
        state.memory["tool_history"] = scenario["inject_tool_history"]

    graph = _build_flow(scenario["flow"])

    if scenario.get("provider_failure"):
        _simulate_provider_failure(state, scenario)

    if not state.runtime.degraded:
        try:
            final_state = graph.run(start="intent_router", state=state)
        except Exception:
            final_state = state
    else:
        final_state = state

    memory_info = _apply_memory_pipeline(final_state)
    mutation_info = _apply_mutation_pipeline(scenario)

    artifact = final_state.world_state.get("artifact")
    artifact_valid = False
    if artifact:
        artifact_valid = artifact.get("status") == "validated"

    recovered = not final_state.runtime.degraded
    if scenario.get("provider_failure"):
        recovered = False

    return {
        "scenario_id": scenario["scenario_id"],
        "system": "numax",
        "flow": scenario["flow"],
        "task_success": final_state.final_output is not None,
        "artifact_valid": artifact_valid,
        "recovered": recovered,
        "continuity_score": memory_info["continuity_score"],
        "cost_used_usd": final_state.budget.cost_used_usd,
        "tokens_used": final_state.budget.tokens_used,
        "rollback_ok": mutation_info["rollback_ok"],
        "replay_ok": mutation_info["replay_ok"],
        "trace_count": len(final_state.trace),
        "fsm_state": final_state.runtime.fsm_state,
        "has_plan": final_state.plan is not None,
        "final_output": final_state.final_output,
        "artifact": artifact,
        "promoted_episodic_count": memory_info["promoted_episodic_count"],
        "semantic_count": memory_info["semantic_count"],
        "memory_policy": memory_info["memory_policy"],
        "mutation_notes": mutation_info["mutation_notes"],
    }
