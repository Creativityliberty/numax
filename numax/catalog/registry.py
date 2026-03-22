from __future__ import annotations

from typing import Any, Dict, List

from numax.catalog.profile_adapter import skill_to_profile
from numax.catalog.recipe_adapter import skill_to_recipe
from numax.catalog.skill_adapter import adapt_skill_to_catalog_item
from numax.catalog.team_adapter import skill_to_team_template


CATALOG_SOURCE = [
    {"skill_id": "nanoclaw-forge", "title": "NanoClaw Forge", "description": "Unified meta-skill."},
    {"skill_id": "orchestra-forge", "title": "Orchestra Forge", "description": "Full-stack agent builder."},
    {"skill_id": "kernel-forge", "title": "Kernel Forge", "description": "Multi-tenant kernel builder."},
    {"skill_id": "flow-orchestrator", "title": "Flow Orchestrator", "description": "Tracing, pause/resume, snapshots."},
    {"skill_id": "blueprint-maker", "title": "Blueprint Maker", "description": "Structured blueprints."},
    {"skill_id": "dag-taskview", "title": "DAG Taskview", "description": "DAG and Mermaid visualization."},
    {"skill_id": "artifact-maker", "title": "Artifact Maker", "description": "Multi-format artifact engine."},
    {"skill_id": "pocketflow", "title": "PocketFlow", "description": "Workflows with nodes, async, batch, retries."},
    {"skill_id": "num-agents", "title": "Num Agents", "description": "AI agents with universe-based architecture."},
    {"skill_id": "agent-pocketflow", "title": "Agent PocketFlow", "description": "Hybrid PocketFlow + agents."},
    {"skill_id": "skill-architect", "title": "Skill Architect", "description": "Audit skills with multi-agent pipeline."},
    {"skill_id": "review-pr", "title": "Review PR", "description": "Review GitHub pull requests."},
    {"skill_id": "mcp-builder", "title": "MCP Builder", "description": "Build production MCP servers."},
]

def build_catalog_registry() -> Dict[str, Any]:
    items: List[Dict[str, Any]] = []
    profiles: List[Dict[str, Any]] = []
    recipes: List[Dict[str, Any]] = []
    teams: List[Dict[str, Any]] = []

    for raw in CATALOG_SOURCE:
        item = adapt_skill_to_catalog_item(
            skill_id=raw["skill_id"],
            title=raw["title"],
            description=raw["description"],
        )
        items.append(item)

        profile = skill_to_profile(item)
        if profile:
            profiles.append(profile)

        recipe = skill_to_recipe(item)
        if recipe:
            recipes.append(recipe)

        team = skill_to_team_template(item)
        if team:
            teams.append(team)

    return {
        "items": items,
        "profiles": profiles,
        "recipes": recipes,
        "teams": teams,
    }
