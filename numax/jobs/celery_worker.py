from __future__ import annotations

from typing import Any, Dict

from numax.jobs.queue_adapter import QueueAdapter


class LocalQueueAdapter(QueueAdapter):
    def __init__(self) -> None:
        self._jobs: Dict[str, Dict[str, Any]] = {}

    def enqueue(self, job_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._jobs[job_id] = {
            "job_id": job_id,
            "payload": payload,
            "status": "queued",
        }
        return {"ok": True, "job_id": job_id, "status": "queued", "backend": "local_queue"}

    def status(self, job_id: str) -> Dict[str, Any]:
        return self._jobs.get(job_id, {"ok": False, "error": "job_not_found", "job_id": job_id})
