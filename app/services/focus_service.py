import json
import os

from app.utils.dates import today_iso
from app.paths import META_FILE, DATA_DIR

print("FOCUS SERVICE LOADED", __name__)

def get_meta():
    if not os.path.exists(META_FILE):
        return {}
    with open(META_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_meta(meta: dict):
    DATA_DIR.mkdir(exist_ok=True)

    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

def get_focus_task_id():
    meta = get_meta()
    today = today_iso()

    if meta.get("focus_date") != today:
        return None

    return meta.get("focus_task_id")

def set_focus(task_id: str):
    meta = get_meta()
    today = today_iso()

    if meta.get("focus_task_id"):
        return

    meta["focus_task_id"] = task_id
    meta["focus_date"] = today

    save_meta(meta)


def clear_focus():
    meta = get_meta()
    print(f"Before clear: {meta}")
    meta["focus_task_id"] = None
    meta["focus_date"] = None
    save_meta(meta)
    print(f"After clear: {meta}")