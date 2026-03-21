from fastapi.testclient import TestClient

from numax.server.app import app


def test_jobs_routes_work() -> None:
    client = TestClient(app)

    headers = {"x-numax-roles": "admin"}

    created = client.post(
        "/jobs/",
        json={"flow": "basic_chat", "prompt": "Explain NUMAX"},
        headers=headers,
    )
    assert created.status_code == 200
    job = created.json()

    listed = client.get("/jobs/", headers=headers)
    assert listed.status_code == 200

    run = client.post(f"/jobs/{job['job_id']}/run", headers=headers)
    assert run.status_code == 200
