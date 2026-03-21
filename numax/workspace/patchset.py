from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class FilePatch(BaseModel):
    path: str
    change_type: str  # create, update, delete
    summary: Optional[str] = None
    diff_preview: Optional[str] = None


class PatchSet(BaseModel):
    patch_id: str
    workspace_id: str
    files: List[FilePatch] = Field(default_factory=list)
    status: str = "draft"  # draft, previewed, applied, reverted
    rationale: Optional[str] = None
