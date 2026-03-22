from __future__ import annotations

from typing import Any, List, Optional
from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    flow: str = Field(..., example="basic_chat")
    prompt: Optional[str] = Field(None, example="Hello NUMAX")
    overrides: dict = Field(default_factory=dict)
    workspace_path: Optional[str] = None


class RunResponse(BaseModel):
    run_id: str
    flow: str
    output: Any
    next_action: Optional[str] = None


class LearningStatsResponse(BaseModel):
    group_by: str
    stats: dict


class ModeRecommendationRequest(BaseModel):
    task_type: str = "general"
    candidates: List[str] = ["repo_operator", "research_mode"]


class ModeRecommendationResponse(BaseModel):
    recommended_id: str
    confidence: float
    reason: str
