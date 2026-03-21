from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

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
    flow_name: Optional[str] = None
    owner: Optional[str] = None
    run_id: Optional[str] = None
    retries: int = 0
    degraded: bool = False


class BudgetState(BaseModel):
    max_tokens_total: Optional[int] = None
    max_cost_usd: Optional[float] = None
    tokens_used: int = 0
    cost_used_usd: float = 0.0


class ConfidenceState(BaseModel):
    understanding_confidence: float = 0.0
    source_confidence: float = 0.0
    output_confidence: float = 0.0
    safety_confidence: float = 1.0


class CritiqueState(BaseModel):
    ok: bool = True
    notes: List[str] = Field(default_factory=list)
    confidence: float = 0.0


class TraceEvent(BaseModel):
    node: str
    phase: Literal["prep", "exec", "post", "fallback", "transition", "error"]
    message: str
    data: Dict[str, Any] = Field(default_factory=dict)


class NumaxState(BaseModel):
    goal: Dict[str, Any] = Field(default_factory=dict)
    observation: Dict[str, Any] = Field(default_factory=dict)
    world_state: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(
        default_factory=lambda: {
            "working": {},
            "continuity": {},
        }
    )
    retrieved_context: List[Dict[str, Any]] = Field(default_factory=list)
    plan: Optional[Dict[str, Any]] = None
    candidate_output: Optional[Any] = None
    critique: Optional[CritiqueState] = None
    final_output: Optional[Any] = None
    runtime: RuntimeState = Field(default_factory=RuntimeState)
    budget: BudgetState = Field(default_factory=BudgetState)
    confidence: ConfidenceState = Field(default_factory=ConfidenceState)
    trace: List[TraceEvent] = Field(default_factory=list)

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
