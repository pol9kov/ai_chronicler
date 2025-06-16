import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
def test_add_and_retrieve():
    resp = client.post("/notes/", json={"id": "1", "text": "hello world"})
    assert resp.status_code == 200 and resp.json()["status"] == "ok"

    resp = client.get("/retrieve/", params={"query": "hello"})
    data = resp.json()
    assert "hello world" in data["literal"]
    assert isinstance(data["vector"], list)
