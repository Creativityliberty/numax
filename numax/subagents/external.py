from __future__ import annotations

from typing import Any, Dict, List

from numax.subagents.contracts import ExternalSubagentRequest, ExternalSubagentResponse
from numax.subagents.providers import ExternalSubagentProvider, ExternalSubagentRegistry


class MockExternalRepoWorker(ExternalSubagentProvider):
    subagent_id = "mock_repo_worker"
    description = "Mock bounded repo worker for testing orchestration."

    def invoke(self, request: ExternalSubagentRequest) -> ExternalSubagentResponse:
        proposed_actions: List[str] = []

        if request.mode == "read_only":
            proposed_actions = [
                "inspect_workspace",
                "read_active_files",
                "summarize_findings",
            ]
        elif request.mode == "patch_proposal":
            proposed_actions = [
                "inspect_target_files",
                "draft_patch_proposal",
                "return_patch_preview",
            ]
        elif request.mode == "test_execution":
            proposed_actions = [
                "run_targeted_tests",
                "collect_failures",
                "report_results",
            ]
        else:
            proposed_actions = [
                "inspect_workspace",
                "draft_patch",
                "run_tests",
                "summarize_result",
            ]

        produced_patch = {}
        if request.mode in {"patch_proposal", "full_bounded"} and request.active_files:
            produced_patch = {
                "path": request.active_files[0],
                "mode": "proposal_only",
                "summary": f"Mock proposal for {request.active_files[0]}",
            }

        test_result = {}
        if request.mode in {"test_execution", "full_bounded"}:
            test_result = {
                "ok": True,
                "command": request.context.get("test_command", ["pytest", "-q"]),
                "summary": "Mock external test execution succeeded.",
            }

        return ExternalSubagentResponse(
            ok=True,
            subagent_id=self.subagent_id,
            summary=f"External worker handled task: {request.task}",
            proposed_actions=proposed_actions,
            produced_patch=produced_patch,
            test_result=test_result,
            raw={
                "mode": request.mode,
                "workspace_path": request.workspace_path,
                "active_files": request.active_files,
                "max_steps": request.max_steps,
            },
        )


def build_default_external_subagent_registry() -> ExternalSubagentRegistry:
    registry = ExternalSubagentRegistry()
    registry.register(MockExternalRepoWorker())
    return registry
