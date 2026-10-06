import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@patch("api.app.generate_headlines")
def test_generate_headlines_success(mock_generate):
    mock_generate.return_value = [
        "Headline 1",
        "Headline 2",
        "Headline 3",
        "Headline 4",
        "Headline 5",
    ]

    response = client.post(
        "/api/generate-headlines", json={"keywords": "woman, river, computer"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["keywords"] == "woman, river, computer"
    assert len(data["headlines"]) == 5
    assert data["headlines"][0] == "Headline 1"


def test_generate_headlines_empty():
    response = client.post("/api/generate-headlines", json={"keywords": "   "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Ключевые слова не могут быть пустыми"


def test_generate_headlines_invalid_payload():
    response = client.post("/api/generate-headlines", json={"wrong_param": "test"})
    assert response.status_code == 422
