from __future__ import annotations

from typing import Dict

from numax.recipes.specs import RecipeSpec


class RecipeRegistry:
    def __init__(self) -> None:
        self._recipes: Dict[str, RecipeSpec] = {}

    def register(self, recipe: RecipeSpec) -> None:
        self._recipes[recipe.recipe_id] = recipe

    def get(self, recipe_id: str) -> RecipeSpec:
        if recipe_id not in self._recipes:
            raise KeyError(f"Unknown recipe: {recipe_id}")
        return self._recipes[recipe_id]

    def list_ids(self) -> list[str]:
        return sorted(self._recipes.keys())


def build_default_recipe_registry() -> RecipeRegistry:
    registry = RecipeRegistry()

    registry.register(
        RecipeSpec(
            recipe_id="workspace_audit",
            title="Workspace Audit",
            description="Open a workspace, index it, and summarize its active files.",
            flow="workspace_analysis",
            profile_id="repo_operator",
            skills=[],
            default_observation={},
            recommended_commands=[
                "numax workspace-scan --path .",
            ],
            constraints=[
                "Read-first operation",
                "No write required",
            ],
        )
    )

    registry.register(
        RecipeSpec(
            recipe_id="repo_repair_basic",
            title="Repo Repair Basic",
            description="Search target code, propose patch, run tests, and review result.",
            flow="repo_repair",
            profile_id="repo_operator",
            skills=["critic_strict"],
            default_observation={
                "preview_patch": True,
                "test_command": ["pytest", "-q"],
            },
            recommended_commands=[
                "numax workspace-repair --path . --query 'failing test' --preview-patch True",
            ],
            constraints=[
                "Patch should remain bounded",
                "Tests should be executed before accepting change",
            ],
        )
    )

    registry.register(
        RecipeSpec(
            recipe_id="benchmark_hardening_run",
            title="Benchmark Hardening Run",
            description="Apply stricter runtime posture and run benchmark proof flow.",
            flow="benchmark_run",
            profile_id="benchmark_hardening",
            skills=["critic_strict"],
            default_observation={},
            recommended_commands=[
                "numax benchmark-run",
            ],
            constraints=[
                "Use stricter critic",
                "Minimize retry count",
            ],
        )
    )

    registry.register(
        RecipeSpec(
            recipe_id="safe_demo_sequence",
            title="Safe Demo Sequence",
            description="Use conservative profile for a bounded demonstration run.",
            flow="artifact_output",
            profile_id="safe_demo_mode",
            skills=[],
            default_observation={
                "artifact_type": "summary",
            },
            recommended_commands=[
                "numax run --flow artifact_output --prompt 'Produce a structured summary'",
            ],
            constraints=[
                "Conservative runtime",
                "No risky tool execution by default",
            ],
        )
    )

    return registry
