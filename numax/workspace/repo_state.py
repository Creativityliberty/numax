from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class RepoFileStatus(BaseModel):
    path: str
    status: str  # modified, added, deleted, untracked, clean


class RepoState(BaseModel):
    branch: Optional[str] = None
    head_commit: Optional[str] = None
    dirty: bool = False
    changed_files: List[RepoFileStatus] = Field(default_factory=list)
