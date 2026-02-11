from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models.task import Task
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.db.models import TaskORM, orm_to_domain, domain_to_orm
from app.infrastructure.db.session import SessionLocal

class SqlAlchemyTaskRepository(TaskRepository):

    def get_all(self) -> list[Task]:
        with SessionLocal() as session:
            result = session.execute(select(TaskORM))
            tasks = result.scalars().all()
            return [orm_to_domain(task) for task in tasks]

    def get_by_id(self, task_id:str) -> Task | None:
        with SessionLocal() as session:
            task = session.get(TaskORM, task_id)
            return orm_to_domain(task) if task else None

    def add(self, task: Task) -> None:
        with SessionLocal() as session:
            orm_task = domain_to_orm(task)
            session.add(orm_task)
            session.commit()

    def update(self, task: Task) -> None:
        with SessionLocal() as session:
            orm_task = session.get(TaskORM, task.id)
            if not orm_task:
                return

            orm_task.text_name = task.text_name
            orm_task.text_description = task.text_description
            orm_task.done = task.done
            orm_task.is_daily = task.is_daily
            orm_task.completed_count = task.completed_count
            orm_task.streak = task.streak
            orm_task.planned_date = task.planned_date
            orm_task.last_completed_date = task.last_completed_date

            session.commit()

    def delete(self, task_id: str) -> None:
        with SessionLocal() as session:
            orm_task = session.get(TaskORM, task_id)
            if not orm_task:
                return
            session.delete(orm_task)
            session.commit()