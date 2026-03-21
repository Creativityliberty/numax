from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RecipeSpec(BaseModel):
    recipe_id: str
    title: str
    description: str = ""
    flow: str
    profile_id: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    default_observation: Dict[str, Any] = Field(default_factory=dict)
    recommended_commands: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
