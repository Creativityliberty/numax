from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class WorkspaceContext(BaseModel):
    workspace_id: str
    root_path: str
    project_name: Optional[str] = None
    repo_type: str = "git"
    active_branch: Optional[str] = None
    active_files: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
