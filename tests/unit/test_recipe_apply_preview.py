from numax.recipes.apply import apply_recipe


def test_apply_recipe_preview():
    result = apply_recipe("safe_demo_sequence", preview=True)

    assert result.ok is True
    assert result.recipe_id == "safe_demo_sequence"
    assert result.execution_plan["flow"] == "artifact_output"
