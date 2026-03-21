from numax.jobs.repo import JobRepository
from numax.jobs.service import JobService
from numax.jobs.worker import LocalJobWorker
from numax.storage.memory_store import InMemoryStore


def test_local_job_worker_runs_one() -> None:
    repo = JobRepository(InMemoryStore())
    service = JobService(repo)
    worker = LocalJobWorker(repo)

    job = service.create_job("basic_chat", "Explain NUMAX")
    result = worker.run_one(job["job_id"])

    assert "job" in result
    assert result["job"]["status"] in {"succeeded", "failed"}
