"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint(client):
    """Test health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_endpoint(client):
    """Test prediction endpoint."""
    response = client.post("/api/predict/", json={
        "events": [{"src_ip": "192.168.1.1", "dst_ip": "10.0.0.1"}]
    })
    assert response.status_code == 200
    assert "predictions" in response.json()


def test_monitor_status(client):
    """Test monitoring status."""
    response = client.get("/api/monitor/status")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_monitor_metrics(client):
    """Test metrics endpoint."""
    response = client.get("/api/monitor/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_events_processed" in data


def test_response_action(client):
    """Test response action."""
    response = client.post(
        "/api/response/action",
        params={"action": "block_ip", "target": "203.0.113.1"}
    )
    assert response.status_code == 200
    assert "action_id" in response.json()
