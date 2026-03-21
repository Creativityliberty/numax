from __future__ import annotations

from typing import Any, Dict, List

from numax.core.node import NumaxNode
from numax.core.state import NumaxState
from numax.tools.file_reader import read_file
from numax.tools.patch_apply import apply_text_patch
from numax.tools.test_runner import run_tests


class WorkspaceTargetSelectNode(NumaxNode):
    name = "workspace_target_select"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "search_result": state.world_state.get("workspace_search", {}),
            "active_workspace": state.active_workspace,
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        matches = payload["search_result"].get("results", [])
        selected = []
        seen = set()

        for item in matches:
            path = item["path"]
            if path in seen:
                continue
            selected.append(path)
            seen.add(path)
            if len(selected) >= 5:
                break

        return {"selected_files": selected}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.active_files = result["selected_files"]
        state.next_recommended_action = "read_target_files"
        state.add_trace(self.name, "post", "Target files selected", files=result["selected_files"])
        return "read"


class WorkspaceReadTargetsNode(NumaxNode):
    name = "workspace_read_targets"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        root = state.active_workspace.get("root_path", ".")
        return {
            "root_path": root,
            "active_files": state.active_files,
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        from pathlib import Path
        files = []
        for rel in payload["active_files"]:
            result = read_file(str((Path(payload["root_path"]) / rel).resolve()))
            if result.get("ok"):
                files.append(
                    {
                        "path": rel,
                        "content": result["content"],
                        "size_bytes": result["size_bytes"],
                    }
                )
        return {"files": files}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.world_state["target_files_content"] = result["files"]
        state.next_recommended_action = "propose_patch"
        state.add_trace(self.name, "post", "Target files read", file_count=len(result["files"]))
        return "propose"


class WorkspacePatchProposalNode(NumaxNode):
    name = "workspace_patch_proposal"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "files": state.world_state.get("target_files_content", []),
            "raw_input": state.observation.get("raw_input", ""),
            "patch_old_text": state.observation.get("patch_old_text"),
            "patch_new_text": state.observation.get("patch_new_text"),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        files = payload["files"]
        if not files:
            return {"proposal": {"ok": False, "reason": "no_target_files"}}

        first = files[0]
        old_text = payload.get("patch_old_text")
        new_text = payload.get("patch_new_text")

        if old_text and new_text:
            proposal = {
                "ok": True,
                "path": first["path"],
                "old_text": old_text,
                "new_text": new_text,
                "mode": "direct_text_replace",
                "rationale": payload["raw_input"],
            }
        else:
            lines = first["content"].splitlines()
            if not lines:
                return {"proposal": {"ok": False, "reason": "empty_file"}}

            old_text = lines[0]
            new_text = lines[0] + "  # NUMAX_PATCH"
            proposal = {
                "ok": True,
                "path": first["path"],
                "old_text": old_text,
                "new_text": new_text,
                "mode": "heuristic_first_line_patch",
                "rationale": payload["raw_input"],
            }

        return {"proposal": proposal}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.last_patch = result["proposal"]
        state.next_recommended_action = "apply_patch_preview"
        state.add_trace(self.name, "post", "Patch proposal created", proposal=result["proposal"])
        return "apply"


class WorkspacePatchApplyNode(NumaxNode):
    name = "workspace_patch_apply"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        root = state.active_workspace.get("root_path", ".")
        proposal = state.last_patch or {}
        return {
            "root_path": root,
            "proposal": proposal,
            "preview_only": state.observation.get("preview_patch", True),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        from pathlib import Path
        proposal = payload["proposal"]
        if not proposal.get("ok"):
            return {"patch_result": {"ok": False, "error": "invalid_proposal"}}

        abs_path = str((Path(payload["root_path"]) / proposal["path"]).resolve())

        patch_result = apply_text_patch(
            path=abs_path,
            old_text=proposal["old_text"],
            new_text=proposal["new_text"],
            preview_only=payload["preview_only"],
        )
        return {"patch_result": patch_result}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.last_patch = {
            **(state.last_patch or {}),
            "apply_result": result["patch_result"],
        }
        state.next_recommended_action = "run_tests"
        state.add_trace(self.name, "post", "Patch apply executed", result=result["patch_result"])
        return "test"


class WorkspaceRunTestsNode(NumaxNode):
    name = "workspace_run_tests"

    def prep(self, state: NumaxState) -> Dict[str, Any]:
        return {
            "root_path": state.active_workspace.get("root_path", "."),
            "command": state.observation.get("test_command", ["pytest", "-q"]),
        }

    def exec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        result = run_tests(
            root_path=payload["root_path"],
            command=payload["command"],
        )
        return {"test_result": result}

    def post(self, state: NumaxState, payload: Dict[str, Any], result: Dict[str, Any]) -> str:
        state.last_test_run = result["test_result"]
        if not result["test_result"].get("ok", False):
            state.last_failure = result["test_result"]
            state.next_recommended_action = "inspect_test_failure"
        else:
            state.next_recommended_action = "critic_review"
        state.add_trace(self.name, "post", "Tests executed", ok=result["test_result"].get("ok", False))
        return "done"
