from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class RuntimeProfile(BaseModel):
    profile_id: str
    title: str
    description: str = ""
    skills: List[str] = Field(default_factory=list)
    config_overrides: Dict[str, Any] = Field(default_factory=dict)
    model_preferences: Dict[str, str] = Field(default_factory=dict)
    router_keywords: List[str] = Field(default_factory=list)
    critic_policy: Dict[str, Any] = Field(default_factory=dict)
