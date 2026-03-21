from __future__ import annotations

from numax.artifacts.schema import Artifact


def render_artifact_text(artifact: Artifact) -> str:
    return (
        f"Artifact ID: {artifact.artifact_id}\n"
        f"Type: {artifact.artifact_type}\n"
        f"Title: {artifact.title}\n"
        f"Status: {artifact.status}\n\n"
        f"Content:\n{artifact.content}\n"
    )


def render_artifact_markdown(artifact: Artifact) -> str:
    return (
        f"# {artifact.title}\n\n"
        f"- **Artifact ID**: {artifact.artifact_id}\n"
        f"- **Type**: {artifact.artifact_type}\n"
        f"- **Status**: {artifact.status}\n\n"
        f"## Content\n\n"
        f"{artifact.content}\n"
    )
