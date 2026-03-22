from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class HandoverRecord(BaseModel):
    from_team: str
    to_team: str
    artifact_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    accepted: bool = True
    notes: List[str] = Field(default_factory=list)


def validate_handover(
    from_team: str,
    to_team: str,
    artifact_type: str,
    payload: Dict[str, Any],
) -> HandoverRecord:
    notes: List[str] = []
    accepted = True

    if not payload:
        accepted = False
        notes.append("Handover payload is empty.")

    if artifact_type == "spec" and "objective" not in payload:
        accepted = False
        notes.append("Spec handover missing objective.")

    if artifact_type == "patch" and "path" not in payload:
        accepted = False
        notes.append("Patch handover missing path.")

    if artifact_type == "review" and "decision" not in payload:
        accepted = False
        notes.append("Review handover missing decision.")

    return HandoverRecord(
        from_team=from_team,
        to_team=to_team,
        artifact_type=artifact_type,
        payload=payload,
        accepted=accepted,
        notes=notes,
    )
