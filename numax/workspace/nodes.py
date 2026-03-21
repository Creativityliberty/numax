from __future__ import annotations

from typing import Any, Dict

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.workspace.service import WorkspaceService


class WorkspaceOpenNode(NumaxNode):
    name = "workspace_open"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        root_path = state.observation.get("workspace_path", ".")
        project_name = state.observation.get("project_name")
        return {
            "root_path": root_path,
            "project_name": project_name,
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        service = WorkspaceService()
        context = service.open_workspace(
            root_path=payload["root_path"],
            project_name=payload.get("project_name"),
        )
        return {"workspace": context.model_dump()}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.active_workspace = result["workspace"]
        state.add_trace(self.name, "post", "Workspace opened", workspace=result["workspace"])
        return "indexed"


class WorkspaceIndexNode(NumaxNode):
    name = "workspace_index"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {"root_path": state.active_workspace.get("root_path", ".")}

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        service = WorkspaceService()
        file_index = service.build_file_index(payload["root_path"])
        return {"file_index": file_index.model_dump()}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        files = result["file_index"]["files"]
        state.world_state["file_index"] = result["file_index"]
        state.active_files = [f["path"] for f in files[:20]]
        state.next_recommended_action = "analyze_active_files"
        state.add_trace(self.name, "post", "Workspace indexed", file_count=len(files))
        return "summarize"


class WorkspaceSummarizeNode(NumaxNode):
    name = "workspace_summarize"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "workspace": state.active_workspace,
            "active_files": state.active_files,
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        text = (
            f"Workspace '{payload['workspace'].get('project_name')}' opened. "
            f"{len(payload['active_files'])} active files selected."
        )
        return {"summary": {"text": text}}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.final_output = result["summary"]
        state.runtime.fsm_state = "DELIVER"
        state.add_trace(self.name, "post", "Workspace summary produced")
        return "done"
