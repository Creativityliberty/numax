from __future__ import annotations

from typing import Any, Dict


def schedule_retry(job_id: str, retries: int, max_retries: int = 3) -> Dict[str, Any]:
    if retries >= max_retries:
        return {
            "ok": False,
            "job_id": job_id,
            "decision": "stop",
            "reason": "retry_budget_exhausted",
        }

    return {
        "ok": True,
        "job_id": job_id,
        "decision": "retry",
        "next_retry": retries + 1,
    }
