from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

from numax.recipes.loader import load_recipe

router = APIRouter()

RECIPES_DIR = Path("recipes")


@router.get("/")
def list_recipes() -> list[dict]:
    if not RECIPES_DIR.exists():
        return []

    rows = []
    for file in RECIPES_DIR.glob("*.json"):
        try:
            rows.append(load_recipe(str(file)))
        except Exception:
            continue
    return rows


@router.get("/{recipe_id}")
def get_recipe(recipe_id: str) -> dict:
    path = RECIPES_DIR / f"{recipe_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Recipe not found")

    try:
        return load_recipe(str(path))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
