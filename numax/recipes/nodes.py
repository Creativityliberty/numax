from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.recipes.apply import apply_recipe


class RecipeApplyNode(NumaxNode):
    name = "recipe_apply"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "recipe_id": state.observation.get("recipe_id", ""),
            "preview": state.observation.get("recipe_preview", True),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        result = apply_recipe(
            recipe_id=payload["recipe_id"],
            preview=payload["preview"],
        )
        return {
            "recipe_apply_result": {
                "ok": result.ok,
                "recipe_id": result.recipe_id,
                "execution_plan": result.execution_plan,
                "notes": result.notes,
            }
        }

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        apply_result = result["recipe_apply_result"]
        state.recipe_apply_result = apply_result

        if apply_result["ok"]:
            state.active_recipe = apply_result["recipe_id"]
            state.recipe_history.append(apply_result["recipe_id"])
            state.world_state["recipe_execution_plan"] = apply_result["execution_plan"]
            state.next_recommended_action = "execute_recipe_flow"
        else:
            state.next_recommended_action = "inspect_recipe_failure"

        state.add_trace(
            self.name,
            "post",
            "Recipe application completed",
            result=apply_result,
        )
        return "done"
