from app.domain.exceptions import TaskNotFoundError, CannotFocusCompletedTaskError, FocusAlreadySetError
from app.domain.repositories.task_repository import TaskRepository
from app.domain.repositories.meta_repository import MetaRepository
from app.utils.dates import today_iso


class FocusService:

    def __init__(
            self,
            task_repository: TaskRepository,
            meta_repository: MetaRepository
    ):
        self._task_repository = task_repository
        self._meta_repository = meta_repository


    def set_focus(self, task_id: str) -> None:
        today = today_iso()

        task = self._task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError("Task not found")

        if task.done:
            raise CannotFocusCompletedTaskError("Cannot set focus on completed task")

        existing_focus = self._meta_repository.get("focus_task_id")
        focus_date = self._meta_repository.get("focus_date")

        if existing_focus and focus_date == today:
            raise FocusAlreadySetError("Focus already set for today")

        self._meta_repository.set("focus_task_id", task_id)
        self._meta_repository.set("focus_date", today)

    def clear_focus(self) -> None:
        self._meta_repository.set("focus_task_id", None)
        self._meta_repository.set("focus_date", None)

    def get_focus(self) -> str | None:
        today = today_iso()
        focus_id = self._meta_repository.get("focus_task_id")
        focus_date = self._meta_repository.get("focus_date")

        if not focus_id:
            return None

        if focus_date != today:
            return None

        return focus_id