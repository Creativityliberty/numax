from __future__ import annotations

from typing import Any, Dict, List, Literal

from pydantic import BaseModel, Field


TrustLevel = Literal["untrusted", "trusted", "verified"]


class PackSpec(BaseModel):
    pack_id: str
    title: str
    publisher: str
    trust_level: TrustLevel = "untrusted"
    profiles: List[str] = Field(default_factory=list)
    recipes: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    signature: str | None = None
