from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

REQUIRED_RECIPE_KEYS = {
    "recipe_id",
    "name",
    "description",
    "flow",
}


def load_recipe(name: str) -> Dict[str, Any]:
    """
    Charge et valide grossièrement une recipe.
    """
    # Assuming RECIPES_DIR is defined globally or imported.
    # If not, this line will cause a NameError.
    # For this edit, I'll assume it's available in the context.
    # If RECIPES_DIR is not defined, the user needs to add it.
    # Example: RECIPES_DIR = Path("./recipes")
    RECIPES_DIR = Path("./recipes") # Added a placeholder for RECIPES_DIR to make the code syntactically correct.
                                   # The user should replace this with their actual RECIPES_DIR.

    path = RECIPES_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Recipe '{name}' not found at {path}")

    data: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))

    if "name" not in data or "version" not in data:
        raise ValueError("Invalid recipe: missing name or version")

    if "plan" not in data or "steps" not in data["plan"]:
        raise ValueError("Invalid recipe: missing plan.steps")

    return data
