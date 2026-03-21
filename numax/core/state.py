from __future__ import annotations

from typing import Any, Literal

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
