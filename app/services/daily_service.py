from datetime import date
from app.domain.repositories.task_repository import TaskRepository
from app.domain.repositories.meta_repository import MetaRepository

class DailyService:

    def __init__(
            self,
            task_repository: TaskRepository,
            meta_repository: MetaRepository
    ):

        self._task_repository = task_repository
        self._meta_repository = meta_repository

    def reset_if_needed(self) -> None:
        today = date.today().isoformat()
        last_reset = self._meta_repository.get("last_reset")

        if last_reset == today:
            return

        tasks = self._task_repository.get_all()

        for task in tasks:
            if task.is_daily:
                task.reset_daily()
                self._task_repository.update(task)

        self._meta_repository.set("last_reset", today)