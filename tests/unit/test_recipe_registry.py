from numax.recipes.registry import build_default_recipe_registry


def test_default_recipe_registry_has_core_recipes():
    registry = build_default_recipe_registry()
    ids = registry.list_ids()

    assert "workspace_audit" in ids
    assert "repo_repair_basic" in ids
