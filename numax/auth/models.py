from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

RoleName = Literal[
    "admin",
    "builder",
    "operator",
    "viewer",
]


class UserIdentity(BaseModel):
    user_id: str
    email: str | None = None
    display_name: str | None = None
    roles: list[RoleName] = Field(default_factory=list)
    is_active: bool = True
