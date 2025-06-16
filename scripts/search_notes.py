from app.memory.vector_memory import VectorMemory

vm = VectorMemory()
query = input("Введите поисковый запрос: ")
res = vm.search(query)
for r in res:
    print("--------")
    print(r["text"][:300])

