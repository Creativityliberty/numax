from fastapi.testclient import TestClient

from numax.server.app import app


def test_sandbox_exec_route_admin() -> None:
    client = TestClient(app)
    response = client.post(
        "/sandbox/exec",
        headers={"x-numax-roles": "admin"},
        json={"command": ["echo", "hello"]},
    )
    assert response.status_code == 200
    assert response.json()["ok"] is True
