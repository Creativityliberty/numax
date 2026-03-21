from __future__ import annotations

from numax.jobs.repo import JobRepository
from numax.jobs.runtime_bridge import run_job_flow
from numax.jobs.specs import JobSpec


class LocalJobWorker:
    def __init__(self, repo: JobRepository) -> None:
        self.repo = repo

    def run_one(self, job_id: str) -> dict:
        payload = self.repo.get(job_id)
        if not payload:
            return {"ok": False, "error": "job_not_found"}

        job = JobSpec(**payload)
        job.status = "running"
        self.repo.save(job)

        result = run_job_flow(flow=job.flow, prompt=job.prompt, metadata=job.metadata)

        if result.get("ok"):
            job.status = "succeeded"
        else:
            job.status = "failed"
        self.repo.save(job)

        return {
            "job": job.model_dump(),
            "result": result,
        }
