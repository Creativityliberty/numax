from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from numax.teams.specs import TeamMission


class TeamState(BaseModel):
    team_id: str
    active_mission: Optional[TeamMission] = None
    local_memory: Dict[str, Any] = Field(default_factory=dict)
    produced_artifacts: List[Dict[str, Any]] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    status: str = "idle"  # idle | ready | running | blocked | done
