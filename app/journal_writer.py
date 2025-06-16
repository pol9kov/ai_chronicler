import os
import datetime
from app.config import Config

class JournalWriter:
    @staticmethod
    def get_directory() -> str:
        cfg = Config.load()
        return os.path.join(cfg["vault_path"], cfg["journal_dir"])

    @staticmethod
    def get_path_for_date(date_str: str) -> str:
        return os.path.join(JournalWriter.get_directory(), f"{date_str}.md")

    @staticmethod
    def date_from_path(path: str) -> str:
        filename = os.path.basename(path)
        name, ext = os.path.splitext(filename)
        if ext != ".md":
            raise ValueError("Not a markdown file")
        return name

    @staticmethod
    def create_for_date(date_str: str) -> None:
        path = JournalWriter.get_path_for_date(date_str)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# Журнал за {date_str}\n\n")

    @staticmethod
    def append_message(role: str, message: str) -> None:
        today = datetime.date.today().isoformat()
        path = JournalWriter.get_path_for_date(today)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} — **{role}**: {message}\n")
