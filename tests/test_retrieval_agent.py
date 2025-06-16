from app.agents.retrieval_agent import RetrievalAgent

class DummyMem:
    def get_notes(self): return ["n1","n2"]
class DummyVec:
    def search(self, q, n_results=5): return ["v1","v2"]

def test_retrieve_combines():
    agent = RetrievalAgent(DummyMem(), DummyVec())
    res = agent.retrieve("query")
    assert res["literal"] == ["n1","n2"]
    assert res["vector"]  == ["v1","v2"]
