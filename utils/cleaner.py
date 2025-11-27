import os
import shutil
from datetime import datetime, timedelta

# Urcă un nivel din folderul utils/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOURCE_DIR = BASE_DIR
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
DAYS_TO_KEEP = 7

os.makedirs(ARCHIVE_DIR, exist_ok=True)

def is_old(path, days):
    mod_time = datetime.fromtimestamp(os.path.getmtime(path))
    return datetime.now() - mod_time > timedelta(days=days)

# Mută toate folderele care încep cu results_data_ în archive/
for item in os.listdir(SOURCE_DIR):
    item_path = os.path.join(SOURCE_DIR, item)
    if os.path.isdir(item_path) and item.startswith("results_data_"):
        dest_path = os.path.join(ARCHIVE_DIR, item)

        # dacă deja există în archive → îl ștergem ca să nu dea eroare
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)

        shutil.move(item_path, dest_path)
        print(f"[MOVED] {item} → {dest_path}")

# Șterge folderele din archive/ mai vechi de 7 zile
for item in os.listdir(ARCHIVE_DIR):
    item_path = os.path.join(ARCHIVE_DIR, item)
    if os.path.isdir(item_path) and is_old(item_path, DAYS_TO_KEEP):
        shutil.rmtree(item_path)
        print(f"[DELETED] {item} (older than {DAYS_TO_KEEP} days)")
