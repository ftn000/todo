import json
import os
from datetime import date
from storage import load_tasks, save_tasks
from utils.dates import today_iso


META_FILE =  "data/meta.json"

def get_last_reset_date():
    if not os.path.exists(META_FILE):
        return None

    with open(META_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("last_reset")

def set_last_reset_date(value: str):
    os.makedirs("data", exist_ok=True)

    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_reset": value}, f)


def reset_daily_tasks():
    today = today_iso()
    last_reset = get_last_reset_date()

    if last_reset == today:
        return

    tasks = load_tasks()

    for task in tasks:
        if task.is_daily:
            task.done = False

    save_tasks(tasks)
    set_last_reset_date(today)