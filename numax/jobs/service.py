from __future__ import annotations

import uuid

from numax.jobs.celery_worker import LocalQueueAdapter
from numax.jobs.repo import JobRepository
from numax.jobs.specs import JobSpec


class JobService:
    def __init__(self, repo: JobRepository) -> None:
        self.repo = repo
        self.queue = LocalQueueAdapter()

    def create_job(self, flow: str, prompt: str, metadata: dict | None = None) -> dict:
        job = JobSpec(
            job_id=str(uuid.uuid4()),
            flow=flow,
            prompt=prompt,
            status="queued",
            metadata=metadata or {},
        )
        self.repo.save(job)
        self.queue.enqueue(job.job_id, job.model_dump())
        return job.model_dump()
