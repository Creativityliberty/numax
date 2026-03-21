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


def load_recipe(path: str) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        raise FileNotFoundError(f"Recipe file not found: {path}")

    data = json.loads(target.read_text(encoding="utf-8"))

    missing = REQUIRED_RECIPE_KEYS.difference(data.keys())
    if missing:
        raise ValueError(f"Recipe missing required keys: {sorted(missing)}")

    return data
