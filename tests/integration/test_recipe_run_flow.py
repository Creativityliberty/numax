from numax.core.state import NumaxState
from numax.flows.recipe_run import build_recipe_run_flow


def test_recipe_run_flow_runs():
    state = NumaxState(
        observation={
            "recipe_id": "workspace_audit",
            "recipe_preview": True,
        }
    )

    graph = build_recipe_run_flow()
    final_state = graph.run(start="recipe_apply", state=state)

    assert final_state.recipe_apply_result
    assert final_state.recipe_apply_result["recipe_id"] == "workspace_audit"
