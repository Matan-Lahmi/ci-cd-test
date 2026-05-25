import json
import pytest
from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_returns_200(client):
    response = client.get("/api/health")
    assert response.status_code == 200


def test_health_returns_ok(client):
    response = client.get("/api/health")
    data = json.loads(response.data)
    assert data == {"status": "ok"}
