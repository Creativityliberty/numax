from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


AssumptionStatus = Literal["explicit", "inferred", "unverified", "invalidated"]


class AssumptionItem(BaseModel):
    statement: str
    status: AssumptionStatus = "inferred"
    impact: str = "medium"  # low | medium | high


class AssumptionMap(BaseModel):
    items: List[AssumptionItem] = Field(default_factory=list)
