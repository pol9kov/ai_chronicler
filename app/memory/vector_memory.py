from sentence_transformers import SentenceTransformer
import chromadb

class VectorMemory:
    """
    Хранит эмбеддинги заметок в Chroma (новый API).
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", persist_path: str = "data/index"):
        self.embed = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection("notes")

    def add_note(self, id: str, text: str):
        vec = self.embed.encode(text).tolist()
        self.collection.add(ids=[id], embeddings=[vec], metadatas=[{"text": text}])

    def search(self, query: str, n_results: int = 5):
        qvec = self.embed.encode(query).tolist()
        res = self.collection.query(query_embeddings=[qvec], n_results=n_results)
        return res["metadatas"][0]
