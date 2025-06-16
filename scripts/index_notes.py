from app.literal_memory import LiteralMemory
from app.memory.vector_memory import VectorMemory

lm = LiteralMemory()
notes = lm.get_all()

vm = VectorMemory()
for idx, (path, text) in enumerate(notes.items()):
    vm.add_note(str(idx), text)
    print(f"Индексировано: {path}")
print("Готово.")

