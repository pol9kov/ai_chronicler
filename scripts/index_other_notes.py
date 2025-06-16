import os
from app.config import Config
from app.memory.vector_memory import VectorMemory

cfg = Config.load()
base = os.path.join(cfg['vault_path'], cfg['journal_dir'])

vm = VectorMemory()

count = 0
for root, _, files in os.walk(base):
    for fn in files:
        if fn.endswith('.md'):
            path = os.path.join(root, fn)
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            if '#Для_ИИ_помощника' not in text:
                vm.add_note(path, text)
                print(f'Индексировано: {path}')
                count += 1
print(f'Готово. Индексировано обычных заметок: {count}')

