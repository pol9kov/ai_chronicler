from fastapi import APIRouter
from pydantic import BaseModel
from app.memory.literal_memory import LiteralMemory
from app.memory.vector_memory import VectorMemory
from app.llm import generate_response
import re

# --- гарантируем get_all() у памяти ---
if not hasattr(LiteralMemory, "get_all"):
    def _get_all(self):
        return getattr(self, "store", {})
    LiteralMemory.get_all = _get_all

router = APIRouter()
lm = LiteralMemory()
vm = VectorMemory()

class ChatMsg(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(msg: ChatMsg):
    user_msg = msg.message

    # --- ищем релевантный контекст ---
    literal_hits = [t for t in lm.get_all().values() if user_msg.lower() in t.lower()]
    if literal_hits:
        context = literal_hits
    else:
        vec_hits = vm.search(user_msg, n_results=3)
        context = [d["text"] for d in vec_hits]

    # --- ответ модели ---
    ai_raw   = generate_response(user_msg, context)
    ai_clean = re.sub(r'\[[^\]]+\]:?', '', ai_raw).strip()

    if context:
        raw = context[0]
        lines = [l.rstrip() for l in raw.splitlines()
                 if l.strip() and l.strip() != "#Для_ИИ_помощника" and not re.fullmatch(r"л+", l)]
        quote = "\n".join(lines).strip()

        # убираем первое вхождение цитаты из ответа (если модель его повторила)
        ai_nodup = ai_clean
        if ai_nodup.startswith(quote):
            ai_nodup = ai_nodup[len(quote):].lstrip()

        answer = f"[Цитата] {quote}\n\n{ai_nodup}"
    else:
        answer = ai_clean

    return {"answer": answer}
