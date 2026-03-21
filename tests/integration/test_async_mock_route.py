from fastapi.testclient import TestClient

from numax.server.app import app


def test_async_providers_route_exists() -> None:
    client = TestClient(app)
    response = client.get("/async/providers")
    assert response.status_code == 200
    assert "providers" in response.json()
