from __future__ import annotations

from typing import Any, Dict


def skill_to_recipe(item: Dict[str, Any]) -> Dict[str, Any] | None:
    skill_id = item["skill_id"]

    mapping = {
        "orchestra-forge": {
            "recipe_id": "orchestra_build_recipe",
            "title": "Orchestra Build Recipe",
            "flow": "director_orchestration",
            "profile_id": "meta_factory",
        },
        "artifact-maker": {
            "recipe_id": "artifact_factory_recipe",
            "title": "Artifact Factory Recipe",
            "flow": "artifact_output",
            "profile_id": "safe_demo_mode",
        },
        "dag-taskview": {
            "recipe_id": "dag_visualization_recipe",
            "title": "DAG Visualization Recipe",
            "flow": "team_map_reduce",
            "profile_id": "flow_runtime",
        },
        "pocketflow": {
            "recipe_id": "pocketflow_workflow_recipe",
            "title": "PocketFlow Workflow Recipe",
            "flow": "team_batch_run",
            "profile_id": "flow_runtime",
        },
    }

    return mapping.get(skill_id)
