import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_pagination():
    # Сбрасываем память между запусками
    client.post("/reset/")
    # Загружаем 10 новых заметок
    for i in range(10):
        client.post("/notes/", json={"id": str(i), "text": f"note{i}"})
    # Запрашиваем с offset=2, limit=3
    resp = client.get(
        "/retrieve/", params={"query": "note", "offset": 2, "limit": 3}
    )
    data = resp.json()
    assert data["literal"] == ["note2", "note3", "note4"]
    assert len(data["vector"]) == 3
