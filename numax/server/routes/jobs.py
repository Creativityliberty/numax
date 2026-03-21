from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from numax.jobs.repo import JobRepository
from numax.jobs.service import JobService
from numax.jobs.worker import LocalJobWorker
from numax.server.middleware.rbac import require_permission
from numax.storage.bootstrap import build_default_store

router = APIRouter()

store = build_default_store()
repo = JobRepository(store)
service = JobService(repo)
worker = LocalJobWorker(repo)


class CreateJobRequest(BaseModel):
    flow: str
    prompt: str
    metadata: dict = Field(default_factory=dict)


@router.post("/")
def create_job(request: Request, payload: CreateJobRequest) -> dict:
    require_permission(request, "jobs.create")
    return service.create_job(payload.flow, payload.prompt, payload.metadata)


@router.get("/")
def list_jobs(request: Request) -> list[dict]:
    require_permission(request, "jobs.read")
    return repo.list_all()


@router.get("/{job_id}")
def get_job(job_id: str, request: Request) -> dict:
    require_permission(request, "jobs.read")
    payload = repo.get(job_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Job not found")
    return payload


@router.post("/{job_id}/run")
def run_job(job_id: str, request: Request) -> dict:
    require_permission(request, "jobs.run")
    result = worker.run_one(job_id)
    if not result.get("ok", True) and result.get("error") == "job_not_found":
        raise HTTPException(status_code=404, detail="Job not found")
    return result
