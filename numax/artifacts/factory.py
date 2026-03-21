from __future__ import annotations

import uuid
from typing import Any

from numax.artifacts.schema import Artifact, ArtifactTrace
from numax.artifacts.types import ArtifactType
from numax.core.state import NumaxState


def build_artifact_from_state(
    state: NumaxState,
    artifact_type: ArtifactType = "summary",
    title: str = "NUMAX Output",
) -> Artifact:
    source_ids: list[str] = []
    if state.retrieved_context:
        source_ids = [item["source_id"] for item in state.retrieved_context if "source_id" in item]

    model_ids: list[str] = []
    if isinstance(state.final_output, dict):
        provider = state.final_output.get("provider")
        model = state.final_output.get("model")
        if provider and model:
            model_ids.append(f"{provider}:{model}")

    content: Any = state.final_output
    if isinstance(content, dict) and "text" in content:
        content = content["text"]

    artifact = Artifact(
        artifact_id=str(uuid.uuid4()),
        artifact_type=artifact_type,
        title=title,
        content=content,
        trace=ArtifactTrace(
            run_id=state.runtime.run_id,
            flow_name=state.runtime.flow_name,
            source_ids=source_ids,
            model_ids=model_ids,
        ),
    )
    return artifact
