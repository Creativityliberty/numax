from __future__ import annotations

from numax.artifacts.schema import Artifact, ArtifactQuality


def validate_artifact(artifact: Artifact) -> Artifact:
    notes = []

    completeness = 1.0 if artifact.content else 0.0
    correctness = 0.7
    traceability = 1.0 if artifact.trace.run_id or artifact.trace.source_ids else 0.4
    format_validity = 1.0 if artifact.title and artifact.artifact_type else 0.0
    style_acceptance = 0.8

    if not artifact.title:
        notes.append("Missing title.")
        format_validity = 0.0

    if not artifact.content:
        notes.append("Missing content.")
        completeness = 0.0
        correctness = 0.0

    artifact.quality = ArtifactQuality(
        completeness=completeness,
        correctness=correctness,
        traceability=traceability,
        format_validity=format_validity,
        style_acceptance=style_acceptance,
    )

    if (
        min(
            artifact.quality.completeness,
            artifact.quality.format_validity,
        )
        < 0.5
    ):
        artifact.status = "invalid"
    else:
        artifact.status = "validated"

    artifact.trace.notes.extend(notes)
    return artifact
