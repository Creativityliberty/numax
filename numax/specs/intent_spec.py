from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class IntentSpec(BaseModel):
    objective: str
    user_request: str
    domain: str = "general"
    task_type: str = "unspecified"
    constraints: List[str] = Field(default_factory=list)
    success_definition: Optional[str] = None
    ambiguity_level: str = "medium"  # low | medium | high
