import json
from typing import List
from app.domain.models.task import Task
from app.paths import DATA_DIR, TASKS_FILE

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
    if not DATA_DIR.exists(DATA_DIR):
        return []

    with open(TASKS_FILE, "r", encoding="utf-8") as f:
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
    DATA_DIR.mkdir(exist_ok=True)

    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [task.__dict__ for task in tasks],
            f,
            ensure_ascii=False,
            indent=2
        )
