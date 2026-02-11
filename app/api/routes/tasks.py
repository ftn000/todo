from fastapi import APIRouter, Form
from fastapi.params import Depends
from fastapi.responses import RedirectResponse

from app.api.dependencies import get_task_repository
from app.domain.repositories.task_repository import TaskRepository
from app.services.task_service import (
    add_task,
    toggle_task,
    delete_task,
    toggle_daily,
)

router = APIRouter()

@router.post("/add")
def create_task(
    text_name: str = Form(..., alias="text-name"),
    text_description: str = Form("", alias="text-description"),
    is_daily: bool = Form(False, alias="is-daily"),
    planned_date: str | None = Form(None, alias="planned-date"),
    repos: TaskRepository = Depends(get_task_repository)
):
    add_task(
        text_name=text_name,
        text_description=text_description,
        is_daily=is_daily,
        planned_date=planned_date,
        repos=repos
    )
    return RedirectResponse(url="/", status_code=303)


@router.post("/toggle/{task_id}")
def toggle(task_id: str, repos: TaskRepository = Depends(get_task_repository)):
    toggle_task(task_id, repos)
    return RedirectResponse(url="/", status_code=303)


@router.post("/toggle-daily/{task_id}")
def toggle_daily_route(task_id: str, repos: TaskRepository = Depends(get_task_repository)):
    toggle_daily(task_id, repos)
    return RedirectResponse(url="/", status_code=303)


@router.post("/delete/{task_id}")
def delete(task_id: str, repos: TaskRepository = Depends(get_task_repository)):
    delete_task(task_id, repos)
    return RedirectResponse(url="/", status_code=303)
