from fastapi.testclient import TestClient

from numax.server.app import app


def test_whoami_route() -> None:
    client = TestClient(app)
    response = client.get(
        "/admin/whoami",
        headers={"x-numax-user-id": "u1", "x-numax-roles": "builder"}
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == "u1"
