from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


ExternalSubagentMode = Literal[
    "read_only",
    "patch_proposal",
    "test_execution",
    "full_bounded",
]


class ExternalSubagentRequest(BaseModel):
    task: str
    workspace_path: Optional[str] = None
    active_files: List[str] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    mode: ExternalSubagentMode = "read_only"
    max_steps: int = 5


class ExternalSubagentResponse(BaseModel):
    ok: bool
    subagent_id: str
    summary: str = ""
    proposed_actions: List[str] = Field(default_factory=list)
    produced_patch: Dict[str, Any] = Field(default_factory=dict)
    test_result: Dict[str, Any] = Field(default_factory=dict)
    raw: Dict[str, Any] = Field(default_factory=dict)
