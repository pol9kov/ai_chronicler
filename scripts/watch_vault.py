#!/usr/bin/env python3
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scripts.ingest_vault import ingest

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            ingest()

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            ingest()

if __name__ == "__main__":
    vault_path = ingest.__globals__['load_config']()
    observer = Observer()
    observer.schedule(Handler(), str(vault_path), recursive=True)
    observer.start()
    print("Watching vault for changes…")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
