from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from numax.artifacts.types import ArtifactType


class ArtifactQuality(BaseModel):
    completeness: float = 0.0
    correctness: float = 0.0
    traceability: float = 0.0
    format_validity: float = 0.0
    style_acceptance: float = 0.0


class ArtifactTrace(BaseModel):
    run_id: str | None = None
    flow_name: str | None = None
    source_ids: list[str] = Field(default_factory=list)
    model_ids: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class Artifact(BaseModel):
    artifact_id: str
    artifact_type: ArtifactType
    title: str
    content: Any
    metadata: dict[str, Any] = Field(default_factory=dict)
    quality: ArtifactQuality = Field(default_factory=ArtifactQuality)
    trace: ArtifactTrace = Field(default_factory=ArtifactTrace)
    status: str = "draft"
