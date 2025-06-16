#!/usr/bin/env python3
import time, subprocess
from scripts.ingest_vault import ingest, load_config

INTERVAL = 300
def sync_loop():
    vault = load_config()
    while True:
        subprocess.run(["git", "-C", str(vault), "pull"], check=False)
        ingest()
        time.sleep(INTERVAL)
if __name__ == "__main__":
    print("Starting sync…")
    sync_loop()
