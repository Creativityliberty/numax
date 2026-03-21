from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from numax.profiles.apply import apply_profile
from numax.recipes.registry import build_default_recipe_registry
from numax.skills.apply import apply_skill
from numax.learning.mode_feedback import append_mode_feedback


@dataclass
class RecipeApplyResult:
    ok: bool
    recipe_id: str
    execution_plan: dict
    notes: list[str]


def apply_recipe(recipe_id: str, preview: bool = True) -> RecipeApplyResult:
    registry = build_default_recipe_registry()
    recipe = registry.get(recipe_id)

    notes: List[str] = [f"Recipe '{recipe_id}' prepared."]
    execution_plan: Dict[str, Any] = {
        "flow": recipe.flow,
        "profile_id": recipe.profile_id,
        "skills": recipe.skills,
        "default_observation": recipe.default_observation,
        "recommended_commands": recipe.recommended_commands,
        "constraints": recipe.constraints,
    }

    if preview:
        notes.append("Preview only: no persistent profile/skill changes applied.")
        return RecipeApplyResult(
            ok=True,
            recipe_id=recipe_id,
            execution_plan=execution_plan,
            notes=notes,
        )

    if recipe.profile_id:
        profile_result = apply_profile(recipe.profile_id, preview=False)
        notes.append(f"Applied profile '{recipe.profile_id}': ok={profile_result.ok}")

    for skill_id in recipe.skills:
        skill_result = apply_skill(skill_id, preview=False)
        notes.append(f"Applied skill '{skill_id}': ok={skill_result.ok}")

    notes.append("Recipe applied and execution plan prepared.")

    if not preview:
        append_mode_feedback(
            {
                "profile": recipe.profile_id,
                "recipe": recipe_id,
                "success": True,
                "rollback": False,
                "duration_seconds": 0.0,
                "cost_used_usd": 0.0,
                "retries": 0,
                "quality_score": 0.75,
                "event": "recipe_apply",
            }
        )

    return RecipeApplyResult(
        ok=True,
        recipe_id=recipe_id,
        execution_plan=execution_plan,
        notes=notes,
    )
