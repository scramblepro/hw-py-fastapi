from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_read_ads():
    response = client.get("/ads")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_ad():
    response = client.post("/ads", json={"title": "Тест", "description": "Описание", "price": 5000})
    assert response.status_code == 201
    assert response.json()["title"] == "Тест"
