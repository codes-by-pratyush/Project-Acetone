from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "Acetone Backend is running"}


def test_mock_cases_route():
    response = client.get("/cases/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_mock_wallet_trace_route():
    response = client.get("/wallets/0x123/trace")

    assert response.status_code == 200
    body = response.json()
    assert "nodes" in body
    assert "edges" in body
