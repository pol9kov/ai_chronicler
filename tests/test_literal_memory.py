import pytest
from app.memory.literal_memory import LiteralMemory

def test_add_and_get_notes():
    m = LiteralMemory()
    m.add_note("first")
    m.add_note("second")
    assert m.get_notes() == ["first", "second"]
