from fastapi.testclient import TestClient
import pytest

from main import app
from config import settings

client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_empty_qa_is_rejected():
    response = client.post("/qa", json={"text": ""})
    assert response.status_code == 422


def test_qa_route_without_key_returns_clear_error(monkeypatch):
    monkeypatch.setattr(settings, "gemini_api_key", "")
    response = client.post("/qa", json={"text": "What is photosynthesis?"})
    assert response.status_code == 503
    assert "GEMINI_API_KEY" in response.json()["detail"]


@pytest.mark.parametrize(
    "path",
    ["/explain", "/summarize"],
)
def test_ai_routes_require_key(monkeypatch, path):
    monkeypatch.setattr(settings, "gemini_api_key", "")
    response = client.post(path, json={"text": "Explain this."})
    assert response.status_code == 503
    assert "GEMINI_API_KEY" in response.json()["detail"]
