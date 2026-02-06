from datetime import date
from storage import load_tasks, save_tasks
from daily import get_last_reset_date, set_last_reset_date
import json
import os

from utils.dates import today_iso

META_FILE = "data/meta.json"

def get_meta():
    if not os.path.exists(META_FILE):
        return {}
    with open(META_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_meta(meta: dict):
    os.makedirs("data", exist_ok=True)
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

def get_focus_task_id():
    meta = get_meta()
    today = today_iso()

    if meta.get("focus_date") != today:
        return None

    return meta.get("focus_task_id")

def set_focus(task_id: str):
    #tasks = load_tasks()
    #task = next((t for t in tasks if t.id == task_id), None)

    #if not task or task.done or not (task.planned_date == today_iso() or task.planned_date is None):
     #   return

    meta = get_meta()
    today = today_iso()

    print(f"ПЕРЕД: task id: {meta["focus_task_id"]}, date: {meta["focus_date"]}")

    if meta.get("focus_task_id"):
        return

    meta["focus_task_id"] = task_id
    meta["focus_date"] = today

    print(f"ПОСЛЕ: task id: {meta["focus_task_id"]}, date: {meta["focus_date"]}")

    save_meta(meta)

def clear_focus():
    meta = get_meta()
    meta["focus_task_id"] = None
    meta["focus_date"] = None
    print(f"task id: {meta["focus_task_id"]}, date: {meta["focus_date"]}")
    save_meta(meta)