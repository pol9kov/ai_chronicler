from llama_cpp import Llama
from app.config import Config

cfg = Config.load()
model_path = cfg["llm"]["local_model_path"]

# Загружаем модель один раз при старте приложения
llm = Llama(
    model_path=model_path,
    n_ctx=2048,     # при необходимости меньше/больше
    n_threads=4,    # подстрой под своё CPU
)

def generate_response(message: str, context: list[str], max_tokens: int = 128) -> str:
    # Берём максимум одну короткую заметку, чтобы промпт был компактным
    if context:
        context = sorted(context, key=len)[:1]
        ctx_block = "\n\n".join(f"[Контекст] {c[:200]}" for c in context)
    else:
        ctx_block = ""

    prompt = (
        "Ты — ИИ-помощник. ВСЕ дословные вставки помечай тегом [Цитата]."
        f"{ctx_block}\n\n[Вопрос] {message}\n[Ответ]:"
    )

    output = llm(
        prompt,
        max_tokens=max_tokens,
        echo=False,
        temperature=0.7,
        top_p=0.9,
    )
    text = output["choices"][0]["text"].strip()
    if "\[Ответ\]" in text:
        text = text.split("\[Ответ\]:")[-1].strip()
    return text
