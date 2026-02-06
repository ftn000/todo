import json
import os
from typing import List
from models import Task

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "tasks.json")


DEFAULTS = {
    "done": False,
    "is_daily": False,
    "completed_count": 0,
    "streak": 0,
    "planned_date": None,
    "last_completed_date": None,
}


def migrate_task(raw: dict) -> dict:
    for key, value in DEFAULTS.items():
        raw.setdefault(key, value)
    return raw


def load_tasks() -> List[Task]:
    if not os.path.exists(DATA_DIR):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw_tasks = json.load(f)

    migrated = []
    changed = False
    for raw in raw_tasks:
        before = raw.copy()
        raw = migrate_task(raw)
        if raw != before:
            changed = True
        migrated.append(Task(**raw))

    if changed:
        save_tasks(migrated)
    return migrated

def save_tasks(tasks: List[Task]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [task.__dict__ for task in tasks],
            f,
            ensure_ascii=False,
            indent=2
        )
