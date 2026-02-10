import uuid
from typing import List

from app.domain.models.task import Task
from storage import load_tasks, save_tasks
from datetime import date, timedelta

from app.utils.dates import today_iso
from app.services.focus_service import get_focus_task_id, clear_focus


def get_all_tasks() -> List[Task]:
    tasks = load_tasks()

    tasks.sort(key=lambda task: task.done)

    return tasks

def get_grouped_tasks():
    tasks = load_tasks()
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

def add_task(
        text_name: str,
        text_description: str,
        is_daily: bool,
        planned_date: str
) -> None:
    tasks = load_tasks()

    task = Task(
        id = str(uuid.uuid4()),
        text_name=text_name,
        text_description=text_description,
        is_daily=is_daily,
        planned_date=planned_date,
        done=False
    )

    tasks.append(task)
    save_tasks(tasks)

def toggle_task(task_id: str):
    tasks = load_tasks()
    today = date.today()
    focus_id = get_focus_task_id()

    for task in tasks:
        if task.id == task_id:
            was_done = task.done
            task.done = not task.done

            if task.is_daily and not was_done and task.done:
                last = (
                    date.fromisoformat(task.last_completed_date)
                    if task.last_completed_date
                    else None
                )

                if last == today:
                    pass
                elif last == today - timedelta(days=1):
                    task.streak += 1
                else:
                    task.streak = 1

                task.last_completed_date = today.isoformat()

            if task.id == focus_id and task.done:
                clear_focus()

            break

    save_tasks(tasks)


def toggle_daily(task_id:str):
    tasks = load_tasks()

    for task in tasks:
        if task.id == task_id:
            task.is_daily = not task.is_daily
            break

    save_tasks(tasks)

def delete_task(task_id: str):
    tasks = load_tasks()
    tasks = [task for task in tasks if task.id != task_id]
    save_tasks(tasks)

def get_focus_task():
    focus_id = get_focus_task_id()
    if not focus_id:
        return None

    for task in load_tasks():
        if task.id == focus_id:
            return task
    return None