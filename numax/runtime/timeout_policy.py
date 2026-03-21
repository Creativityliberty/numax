from __future__ import annotations

from typing import Any, Dict


def decide_timeout_policy(
    flow_name: str | None,
    task_type: str | None = None,
    degraded: bool = False,
) -> Dict[str, Any]:
    timeout_seconds = 30
    mode = "standard"
    reason = "Default timeout policy."

    if flow_name in {"workspace_search", "specification_loop", "profile_apply"}:
        timeout_seconds = 15
        mode = "fast"
        reason = "Lightweight flow."

    elif flow_name in {"code_change_loop", "repo_repair"}:
        timeout_seconds = 120
        mode = "extended"
        reason = "Repo operations and tests may take longer."

    elif flow_name in {"benchmark_run", "artifact_output"}:
        timeout_seconds = 180
        mode = "heavy"
        reason = "Benchmark/artifact flows are heavier."

    if task_type == "repo_change":
        timeout_seconds = max(timeout_seconds, 120)
        reason = "Repo change task type requires extended timeout."

    if degraded:
        timeout_seconds = min(timeout_seconds, 20)
        mode = "conservative"
        reason = "Runtime degraded: reduce timeout to fail fast."

    return {
        "timeout_seconds": timeout_seconds,
        "mode": mode,
        "reason": reason,
    }
