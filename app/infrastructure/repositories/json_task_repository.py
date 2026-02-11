from app.domain.models.task import Task
from app.domain.repositories.task_repository import TaskRepository
from storage import load_tasks, save_tasks


class JsonTaskRepository(TaskRepository):

    def get_all(self) -> list[Task]:
        return load_tasks()

    def get_by_id(self, task_id:str) -> Task | None:
        tasks = load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def add(self, task: Task) -> None:
        tasks = load_tasks()
        tasks.append(task)
        save_tasks(tasks)

    def update(self, task: Task) -> None:
        tasks = load_tasks()
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task
                break
        save_tasks(tasks)

    def delete(self, task_id: str) -> None:
        tasks = load_tasks()
        tasks = [task for task in tasks if task.id != task_id]
        save_tasks(tasks)
