import uuid
from datetime import date
from typing import List, Optional

from app.infrastructure.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from app.domain.models.task import Task
from app.services.focus_service import get_focus_task_id, clear_focus
from app.utils.dates import today_iso


repos = SqlAlchemyTaskRepository()


def get_all_tasks() -> List[Task]:
    tasks = repos.get_all()
    tasks.sort(key = lambda t:t.done)
    return tasks

def get_grouped_tasks():
    tasks = repos.get_all()
    focus_id = get_focus_task_id()
    today = today_iso()

    daily = []
    active = []
    future = []
    overdue = []
    done = []

    for task in tasks:
        if task.id == focus_id:
            continue

        if task.is_daily:
            daily.append(task)
            continue

        if task.done:
            done.append(task)
            continue

        if task.planned_date is None:
            active.append(task)
            continue

        if task.planned_date > today:
            future.append(task)
        elif task.planned_date == today:
            active.append(task)
        else:
            overdue.append(task)

    return {
        "daily": daily,
        "active": active,
        "future": future,
        "overdue": overdue,
        "done": done
    }

def get_focus_task() -> Optional[Task]:
    tasks = repos.get_all()
    focus_id = get_focus_task_id()
    if not focus_id:
        return None

    for task in tasks:
        if task.id == focus_id:
            return task

    return None


def add_task(
        text_name: str,
        text_description: str,
        is_daily: bool,
        planned_date: Optional[str]
) -> None:


    task = Task(
        id=str(uuid.uuid4()),
        text_name=text_name,
        text_description=text_description,
        is_daily=is_daily,
        planned_date=planned_date if not is_daily else None
    )

    repos.add(task)

def toggle_task(task_id: str):
    task = repos.get_by_id(task_id)
    today = date.today()
    focus_id = get_focus_task_id()

    if not task:
        return

    if task.done:
        task.mark_undone()
    else:
        task.mark_done(today)

    if task.id == focus_id:
        clear_focus()

    repos.update(task)

def toggle_daily(task_id: str) -> None:
    task = repos.get_by_id(task_id)
    if not task:
        return

    task.toggle_daily()
    repos.update(task)

def delete_task(task_id: str) -> None:
    repos.delete(task_id)