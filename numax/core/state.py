from __future__ import annotations

from typing import Any, Dict, List, Literal

from pydantic import BaseModel, Field

FsmState = Literal[
    "IDLE",
    "UNDERSTAND",
    "PLAN",
    "BUILD",
    "DELIVER",
    "LEARN",
    "DEGRADED",
    "HALT",
]


class RuntimeState(BaseModel):
    fsm_state: FsmState = "IDLE"
    flow_name: str | None = None
    owner: str | None = None
    run_id: str | None = None
    retries: int = 0
    max_retries: int = 3
    degraded: bool = False


class BudgetState(BaseModel):
    max_tokens_total: int | None = None
    max_cost_usd: float | None = None
    tokens_used: int = 0
    cost_used_usd: float = 0.0


class ConfidenceState(BaseModel):
    understanding_confidence: float = 0.0
    source_confidence: float = 0.0
    output_confidence: float = 0.0
    safety_confidence: float = 1.0


class CritiqueState(BaseModel):
    ok: bool = True
    notes: list[str] = Field(default_factory=list)
    confidence: float = 0.0


class TraceEvent(BaseModel):
    node: str
    phase: Literal["prep", "exec", "post", "fallback", "transition", "error"]
    message: str
    data: dict[str, Any] = Field(default_factory=dict)


class NumaxState(BaseModel):
    goal: dict[str, Any] = Field(default_factory=dict)
    observation: dict[str, Any] = Field(default_factory=dict)
    world_state: dict[str, Any] = Field(default_factory=dict)
    memory: dict[str, Any] = Field(
        default_factory=lambda: {
            "working": {},
            "continuity": {},
        }
    )
    retrieved_context: list[dict[str, Any]] = Field(default_factory=list)
    plan: dict[str, Any] | None = None
    candidate_output: Any | None = None
    critique: CritiqueState | None = None
    final_output: Any | None = None
    runtime: RuntimeState = Field(default_factory=RuntimeState)
    budget: BudgetState = Field(default_factory=BudgetState)
    confidence: ConfidenceState = Field(default_factory=ConfidenceState)
    active_workspace: dict[str, Any] = Field(default_factory=dict)
    active_files: list[str] = Field(default_factory=list)
    last_patch: dict[str, Any] = Field(default_factory=dict)
    last_test_run: dict[str, Any] = Field(default_factory=dict)
    last_failure: dict[str, Any] = Field(default_factory=dict)
    next_recommended_action: str | None = None
    code_review: dict[str, Any] = Field(default_factory=dict)
    patch_risk: str | None = None
    change_scope: str | None = None

    # V2 Subagent state
    active_subagent: str | None = None
    subagent_notes: list[str] = Field(default_factory=list)
    subagent_plan: dict[str, Any] = Field(default_factory=dict)

    # V2 Spec state
    intent_spec: dict[str, Any] = Field(default_factory=dict)
    work_spec: dict[str, Any] = Field(default_factory=dict)
    assumptions: dict[str, Any] = Field(default_factory=dict)
    acceptance_criteria: list[str] = Field(default_factory=list)
    spec_status: str | None = None

    # V2 Improvement state
    improvement_suggestions: list[dict[str, Any]] = Field(default_factory=list)
    mutation_decision: dict[str, Any] = Field(default_factory=dict)
    improvement_status: str | None = None

    # V2 Profile state
    active_profile: str | None = None
    profile_history: list[str] = Field(default_factory=list)
    profile_apply_result: dict[str, Any] = Field(default_factory=dict)

    # V2 Runtime Resilience state
    runtime_events: list[dict[str, Any]] = Field(default_factory=list)
    event_buffer_status: dict[str, Any] = Field(default_factory=dict)
    timeout_decision: dict[str, Any] = Field(default_factory=dict)
    runtime_resilience_status: str | None = None

    # V2 Recipe state
    active_recipe: str | None = None
    recipe_history: list[str] = Field(default_factory=list)
    recipe_apply_result: dict[str, Any] = Field(default_factory=dict)

    # V2 External Subagent state
    external_subagent_result: dict[str, Any] = Field(default_factory=dict)
    external_subagent_history: list[dict[str, Any]] = Field(default_factory=list)

    # V2 Learning state
    active_feedback: dict[str, Any] = Field(default_factory=dict)
    mode_recommendation: dict[str, Any] = Field(default_factory=dict)
    learning_history: list[dict[str, Any]] = Field(default_factory=list)
    mode_feedback: list[dict[str, Any]] = Field(default_factory=list)
    mode_selection_result: dict[str, Any] = Field(default_factory=dict)
    
    # V3 Teams state
    teams_state: Dict[str, Any] = Field(default_factory=dict)
    team_results: Dict[str, Any] = Field(default_factory=dict)
    handover_log: List[Dict[str, Any]] = Field(default_factory=list)

    # V3 Blackboard state
    blackboard_state: Dict[str, Any] = Field(default_factory=lambda: {"entries": []})
    mission_queue: Dict[str, Any] = Field(default_factory=lambda: {"messages": []})
    subscription_state: Dict[str, Any] = Field(default_factory=dict)

    # V3 Batch/Parallel state
    batch_results: List[Dict[str, Any]] = Field(default_factory=list)
    parallel_results: List[Dict[str, Any]] = Field(default_factory=list)
    map_reduce_result: Dict[str, Any] = Field(default_factory=dict)

    # V3 Catalog state
    catalog_items: List[Dict[str, Any]] = Field(default_factory=list)
    catalog_sync_result: Dict[str, Any] = Field(default_factory=dict)
    catalog_team_templates: List[Dict[str, Any]] = Field(default_factory=list)

    # V3 Director state
    director_plan: Dict[str, Any] = Field(default_factory=dict)
    director_assignments: List[Dict[str, Any]] = Field(default_factory=list)
    director_results: Dict[str, Any] = Field(default_factory=dict)

    trace: list[TraceEvent] = Field(default_factory=list)

    def add_trace(
        self,
        node: str,
        phase: Literal["prep", "exec", "post", "fallback", "transition", "error"],
        message: str,
        **data: Any,
    ) -> None:
        self.trace.append(
            TraceEvent(
                node=node,
                phase=phase,
                message=message,
                data=data,
            )
        )
