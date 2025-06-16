import pytest
from app.memory.vector_memory import VectorMemory

def test_init_vector_memory(tmp_path, monkeypatch):
    # Подменяем ChromaClient, чтобы не падало
    class DummyClient:
        def create_collection(self, name, persist_directory): return type("C", (), {})()
    monkeypatch.setattr("app.memory.vector_memory.chromadb.Client", lambda: DummyClient())

    vm = VectorMemory(model_name="all-MiniLM-L6-v2", persist_path=str(tmp_path))
    assert hasattr(vm, "add_note")
    assert hasattr(vm, "search")
