from __future__ import annotations

from typing import Any


def build_correlation_context(
    run_id: str | None = None,
    session_id: str | None = None,
    flow_name: str | None = None,
    provider: str | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "session_id": session_id,
        "flow_name": flow_name,
        "provider": provider,
        "model": model,
    }
