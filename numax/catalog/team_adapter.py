from __future__ import annotations

from typing import Any, Dict


def skill_to_team_template(item: Dict[str, Any]) -> Dict[str, Any] | None:
    skill_id = item["skill_id"]

    mapping = {
        "skill-architect": {
            "team_id": "audit_squad",
            "name": "Audit Squad",
            "purpose": "Audit skills, pipelines, and outputs.",
            "default_flow": "subagent_review",
        },
        "review-pr": {
            "team_id": "pr_review_squad",
            "name": "PR Review Squad",
            "purpose": "Review PRs for bugs, design, tests, and security.",
            "default_flow": "subagent_review",
        },
        "artifact-maker": {
            "team_id": "artifact_squad",
            "name": "Artifact Squad",
            "purpose": "Produce and package multi-format outputs.",
            "default_flow": "artifact_output",
        },
        "orchestra-forge": {
            "team_id": "builder_squad",
            "name": "Builder Squad",
            "purpose": "Build full-stack agents and orchestrated pipelines.",
            "default_flow": "director_orchestration",
        },
    }

    return mapping.get(skill_id)
