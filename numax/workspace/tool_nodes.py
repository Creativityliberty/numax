from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.tools.workspace_tools import WorkspaceTools


class WorkspaceSearchNode(NumaxNode):
    name = "workspace_search"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "root_path": state.active_workspace.get("root_path", "."),
            "query": state.observation.get("search_query", state.observation.get("raw_input", "")),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        tools = WorkspaceTools()
        result = tools.search(
            root_path=payload["root_path"],
            query=payload["query"],
        )
        return {"search_result": result}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.world_state["workspace_search"] = result["search_result"]
        matches = result["search_result"].get("results", [])
        state.next_recommended_action = "read_matched_files" if matches else "refine_query"
        state.add_trace(self.name, "post", "Workspace search completed", match_count=len(matches))
        return "done"
