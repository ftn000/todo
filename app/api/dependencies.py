from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository

def get_task_repository() -> TaskRepository:
    return  SqlAlchemyTaskRepository()