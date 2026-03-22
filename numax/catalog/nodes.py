from __future__ import annotations

from typing import Any, Dict

from numax.catalog.registry import build_catalog_registry
from numax.core.node import NumaxNode
from numax.core.state import NumaxState


class CatalogSyncNode(NumaxNode):
    name = "catalog_sync"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {}

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        registry = build_catalog_registry()
        return {"catalog": registry}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        catalog = result["catalog"]
        state.catalog_items = catalog["items"]
        state.catalog_team_templates = catalog["teams"]
        state.catalog_sync_result = {
            "item_count": len(catalog["items"]),
            "profile_count": len(catalog["profiles"]),
            "recipe_count": len(catalog["recipes"]),
            "team_count": len(catalog["teams"]),
        }
        state.world_state["catalog_registry"] = catalog
        state.next_recommended_action = "apply_catalog_capabilities"
        state.add_trace(
            self.name,
            "post",
            "Catalog synchronized",
            result=state.catalog_sync_result,
        )
        return "done"
