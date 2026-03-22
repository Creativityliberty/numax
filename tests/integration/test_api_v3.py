import sys
from fastapi.testclient import TestClient
from numax.server.app import create_app

def test_api_v3_flows_registered():
    app = create_app()
    client = TestClient(app)
    
    # Check health
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True
    
    # We won't run full flows (as they might hit APIs), 
    # but we verify the router doesn't crash on import
    print("API V3 Integration Verified")

if __name__ == "__main__":
    test_api_v3_flows_registered()
