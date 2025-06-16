import glob
import os
import datetime
from app.git_handler import GitHandler
from app.journal_writer import JournalWriter

def handle():
    today = datetime.date.today().isoformat()
    vault = GitHandler()
    vault.pull()

    # Если уже есть файл за сегодня — ничего не делать
    if os.path.exists(JournalWriter.get_path_for_date(today)):
        return

    # Найти все предыдущие журналы и вытянуть даты
    dir_path = JournalWriter.get_directory()
    files = glob.glob(os.path.join(dir_path, '*.md'))
    dates = []
    for f in files:
        try:
            d = JournalWriter.date_from_path(f)
            if d < today:
                dates.append(d)
        except ValueError:
            continue

    # Пушим последний файл перед сегодняшним
    if dates:
        last_date = max(dates)
        vault.commit_and_push(f"journal {last_date}")

    # Создаём файл на сегодня
    JournalWriter.create_for_date(today)
