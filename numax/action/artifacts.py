from __future__ import annotations

from typing import Any

from numax.artifacts.factory import build_artifact_from_state
from numax.artifacts.validators import validate_artifact
from numax.core.node import NumaxNode
from numax.core.state import NumaxState


class ArtifactNode(NumaxNode):
    name = "artifact"

    def prep(self, state: NumaxState) -> dict[str, Any]:
        payload = {
            "artifact_type": state.world_state.get("artifact_type", "summary"),
            "artifact_title": state.world_state.get("artifact_title", "NUMAX Output"),
        }
        state.add_trace(self.name, "prep", "Artifact payload prepared", **payload)
        return payload

    def exec(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "artifact_type": payload["artifact_type"],
            "artifact_title": payload["artifact_title"],
        }

    def post(
        self,
        state: NumaxState,
        payload: dict[str, Any],
        result: dict[str, Any],
    ) -> str:
        artifact = build_artifact_from_state(
            state=state,
            artifact_type=result["artifact_type"],
            title=result["artifact_title"],
        )
        artifact = validate_artifact(artifact)

        state.world_state["artifact"] = artifact.model_dump()
        state.add_trace(
            self.name,
            "post",
            "Artifact created",
            artifact_id=artifact.artifact_id,
            artifact_type=artifact.artifact_type,
            artifact_status=artifact.status,
        )
        return "done"
