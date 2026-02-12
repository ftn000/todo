from pathlib import Path

from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.repositories.json_meta_repository import JsonMetaRepository
from app.infrastructure.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from app.services.daily_service import DailyService
from app.services.focus_service import FocusService
from app.services.task_service import TaskService

app_path = "./data/meta.json"

def get_task_repository() -> TaskRepository:
    return  SqlAlchemyTaskRepository()

def get_task_service() -> TaskService:
    task_repos = SqlAlchemyTaskRepository()
    meta_repos = JsonMetaRepository(Path(app_path))

    focus_service = FocusService(task_repos, meta_repos)

    return TaskService(task_repos, focus_service)

def get_focus_service() -> FocusService:
    task_repos = SqlAlchemyTaskRepository()
    meta_repos = JsonMetaRepository(Path(app_path))

    return FocusService(task_repos, meta_repos)

def get_daily_service() -> DailyService:
    return DailyService(
        task_repository=SqlAlchemyTaskRepository(),
        meta_repository=JsonMetaRepository(Path(app_path))
    )