from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


TeamRole = Literal[
    "lead",
    "operator",
    "coder",
    "reviewer",
    "researcher",
    "qa",
    "release",
]


class TeamMemberSpec(BaseModel):
    member_id: str
    role: TeamRole
    capabilities: List[str] = Field(default_factory=list)
    external_subagent_id: Optional[str] = None


class TeamMission(BaseModel):
    mission_id: str
    title: str
    objective: str
    inputs: Dict[str, Any] = Field(default_factory=dict)
    expected_outputs: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    priority: int = 5


class TeamSpec(BaseModel):
    team_id: str
    name: str
    purpose: str
    members: List[TeamMemberSpec] = Field(default_factory=list)
    default_flow: Optional[str] = None
    supported_missions: List[str] = Field(default_factory=list)
