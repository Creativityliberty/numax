from __future__ import annotations

from typing import Any

from numax.jobs.specs import JobSpec
from numax.storage.base import KeyValueStore


class JobRepository:
    def __init__(self, store: KeyValueStore) -> None:
        self.store = store

    def save(self, job: JobSpec) -> None:
        self.store.set(f"jobs/{job.job_id}", job.model_dump())

    def get(self, job_id: str) -> dict[str, Any] | None:
        res = self.store.get(f"jobs/{job_id}")
        return res if isinstance(res, dict) else None

    def list_all(self) -> list[dict]:
        rows = []
        for key in self.store.list_keys():
            if key.startswith("jobs/"):
                item = self.store.get(key)
                if item:
                    rows.append(item)
        return rows
