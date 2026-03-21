from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

JobStatus = Literal[
    "queued",
    "running",
    "succeeded",
    "failed",
    "cancelled",
]


class JobSpec(BaseModel):
    job_id: str
    flow: str
    prompt: str
    status: JobStatus = "queued"
    metadata: dict[str, Any] = Field(default_factory=dict)
