import uuid
from datetime import date
from typing import List, Optional

from app.domain.exceptions import TaskNotFoundError
from app.domain.repositories.task_repository import TaskRepository
from app.domain.models.task import Task
from app.services.focus_service import FocusService
from app.utils.dates import today_iso, today


class TaskService:
    def __init__(
            self,
            task_repository: TaskRepository,
            focus_repository: FocusService
    ):
        self._task_repository = task_repository
        self._focus_service = focus_repository

    def get_all_tasks(self) -> List[Task]:
        tasks = self._task_repository.get_all()
        tasks.sort(key=lambda t: t.done)
        return tasks

    def get_grouped_tasks(self):
        tasks = self._task_repository.get_all()
        focus_id = self._focus_service.get_focus()
        str_today = today_iso()

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

            if task.planned_date > str_today:
                future.append(task)
            elif task.planned_date == str_today:
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

    def get_focus_task(self) -> Optional[Task]:
        focus_id = self._focus_service.get_focus()
        if not focus_id:
            return None

        return self._task_repository.get_by_id(focus_id)

    def add_task(
            self,
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

        self._task_repository.add(task)

    def toggle_task(self, task_id: str):
        task = self._task_repository.get_by_id(task_id)

        if not task:
            raise TaskNotFoundError("Task not found")

        task.toggle_done(today())

        if task.id == self._focus_service.get_focus():
            self._focus_service.clear_focus()

        self._task_repository.update(task)

    def toggle_daily(self, task_id: str) -> None:
        task = self._task_repository.get_by_id(task_id)
        if not task:
            return

        task.toggle_daily()
        self._task_repository.update(task)

    def delete_task(self, task_id: str) -> None:
        self._task_repository.delete(task_id)