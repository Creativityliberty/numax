from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class DirectedMission(BaseModel):
    mission_id: str
    team_id: str
    title: str
    objective: str
    inputs: Dict[str, Any] = Field(default_factory=dict)
    expected_outputs: List[str] = Field(default_factory=list)


class DirectorPlan(BaseModel):
    objective: str
    missions: List[DirectedMission] = Field(default_factory=list)


class DirectorAssignment(BaseModel):
    team_id: str
    mission_id: str
    accepted: bool = True
    notes: List[str] = Field(default_factory=list)
