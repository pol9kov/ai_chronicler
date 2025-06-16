from fastapi import FastAPI, Query
from app.memory.literal_memory import LiteralMemory
from app.memory.vector_memory import VectorMemory
from app.agents.retrieval_agent import RetrievalAgent

app = FastAPI()

# глобальные экземпляры памяти и агента
literal = LiteralMemory()
vector  = VectorMemory()
agent   = RetrievalAgent(literal, vector)

@app.post("/notes/")
async def add_note(payload: dict):
    literal.add_note(payload["text"])
    vector.add_note(payload["id"], payload["text"])
    return {"status": "ok"}

@app.get("/retrieve/")
async def retrieve(
    query: str  = Query(...),
    offset: int = Query(0, ge=0),
    limit:  int = Query(5, gt=0, le=50)
):
    return agent.retrieve(query, offset=offset, limit=limit)

@app.post("/reset/")
async def reset():
    global literal, vector, agent
    literal = LiteralMemory()
    vector  = VectorMemory()
    agent   = RetrievalAgent(literal, vector)
    return {"status": "reset"}

from app.routers import chat
app.include_router(chat.router)

from app.routers import chat
app.include_router(chat.router)
