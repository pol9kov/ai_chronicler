import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from app.literal_memory import LiteralMemory
from app.memory.vector_memory import VectorMemory
from app.config import Config
import subprocess

def ask_llm(prompt: str, max_tokens: int = 256) -> str:
    cfg = Config.load()
    model_path = cfg['llm']['local_model_path']
    binary = "./llama.cpp/build/bin/llama-cli"
    cmd = [binary, "-m", model_path, "-p", prompt, "-n", str(max_tokens)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def gather_context(user_message: str):
    lm = LiteralMemory()
    literal_matches = [text for text in lm.get_all().values() if user_message.lower() in text.lower()]
    if literal_matches:
        return literal_matches
    vm = VectorMemory()
    vecs = vm.search(user_message, n_results=3)
    return [d["text"] for d in vecs]

def main():
    print("ИИ-помощник запущен. Введите сообщение или exit:")
    while True:
        user_message = input("> ")
        if user_message.lower() in ["exit", "quit"]:
            break
        context = gather_context(user_message)
        system_prompt = "Ты — персональный ИИ-помощник. Если приводишь точную цитату из памяти, пометь её как [Цитата]."
        formatted_context = "\n\n".join(f"[Контекст] {c}" for c in context)
        prompt = f"{system_prompt}\n\n{formatted_context}\n\n[Вопрос пользователя] {user_message}\n[Ответ]:"
        answer = ask_llm(prompt)
        print("ИИ:", answer)

if __name__ == "__main__":
    main()
