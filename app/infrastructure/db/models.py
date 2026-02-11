from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base
from app.domain.models.task import Task


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    text_name: Mapped[str] = mapped_column(String)
    text_description: Mapped[str] = mapped_column(String)

    done: Mapped[bool] = mapped_column(Boolean, default=False)
    is_daily: Mapped[bool] = mapped_column(Boolean, default=False)

    completed_count: Mapped[int] = mapped_column(Integer, default=0)
    streak: Mapped[int] = mapped_column(Integer, default=0)

    planned_date: Mapped[str | None] = mapped_column(String, nullable=True)
    last_completed_date: Mapped[str | None] = mapped_column(String, nullable=True)


class MetaORM(Base):
    __tablename__ = "meta"

    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str | None] = mapped_column(String, nullable=True)


def orm_to_domain(task_orm: TaskORM) -> Task:
    return Task(
        id = task_orm.id,
        text_name=task_orm.text_name,
        text_description=task_orm.text_description,
        done=task_orm.done,
        is_daily=task_orm.is_daily,
        completed_count=task_orm.completed_count,
        streak=task_orm.streak,
        planned_date=task_orm.planned_date,
        last_completed_date=task_orm.last_completed_date
    )

def domain_to_orm(task: Task) -> TaskORM:
    return TaskORM(
        id=task.id,
        text_name=task.text_name,
        text_description=task.text_description,
        done=task.done,
        is_daily=task.is_daily,
        completed_count=task.completed_count,
        streak=task.streak,
        planned_date=task.planned_date,
        last_completed_date=task.last_completed_date
    )