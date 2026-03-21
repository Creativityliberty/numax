from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class WorkSpec(BaseModel):
    title: str
    scope_in: List[str] = Field(default_factory=list)
    scope_out: List[str] = Field(default_factory=list)
    deliverables: List[str] = Field(default_factory=list)
    steps: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    acceptance_criteria: List[str] = Field(default_factory=list)
    ready: bool = False
