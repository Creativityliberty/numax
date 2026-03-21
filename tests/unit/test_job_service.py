from numax.jobs.repo import JobRepository
from numax.jobs.service import JobService
from numax.storage.memory_store import InMemoryStore


def test_job_service_creates_job() -> None:
    repo = JobRepository(InMemoryStore())
    service = JobService(repo)

    job = service.create_job("basic_chat", "Explain NUMAX")

    assert job["flow"] == "basic_chat"
    assert job["status"] == "queued"
