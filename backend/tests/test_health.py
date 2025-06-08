"""
Tests for health check endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


def test_legacy_health_check(client: TestClient):
    """Test legacy health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_basic_health_check(async_client: AsyncClient):
    """Test basic health check endpoint."""
    response = await async_client.get("/api/v1/health/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "MemVoice API"
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_detailed_health_check(async_client: AsyncClient):
    """Test detailed health check endpoint."""
    response = await async_client.get("/api/v1/health/health/detailed")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "checks" in data
    assert "database" in data["checks"]
    assert "configuration" in data["checks"]


@pytest.mark.asyncio
async def test_ping_endpoint(async_client: AsyncClient):
    """Test ping endpoint."""
    response = await async_client.get("/api/v1/health/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_root_endpoint(client: TestClient):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "MemVoice API is running"
    assert "version" in data
    assert "docs_url" in data
    assert "environment" in data 