from app.literal_memory import LiteralMemory

lm = LiteralMemory()
notes = lm.get_all()
print(f"Всего найдено заметок с тегом: {len(notes)}")
for path, text in notes.items():
    print(f"--- {path} ---\n{text[:200]}\n")

