from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns correct response."""
    response = client.get("/")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "MemVoice API is running"
    assert "version" in response_data
    assert "docs_url" in response_data
    assert "environment" in response_data


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_cors_headers():
    """Test that CORS headers are present."""
    response = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    # CORS headers should be present
    assert "access-control-allow-origin" in response.headers
