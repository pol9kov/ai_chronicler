from app.memory.literal_memory import LiteralMemory
from app.memory.vector_memory import VectorMemory

class RetrievalAgent:
    def __init__(self, literal: LiteralMemory, vector: VectorMemory):
        self.literal = literal
        self.vector = vector

    def retrieve(self, query: str, offset: int = 0, limit: int = 5):
        lit = self.literal.get_notes()[offset:offset+limit]
        vec_all = self.vector.search(query, n_results=offset+limit)
        vec = vec_all[offset:offset+limit]
        return {"literal": lit, "vector": vec}
