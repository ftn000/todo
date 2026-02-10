from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse

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
):
    add_task(
        text_name=text_name,
        text_description=text_description,
        is_daily=is_daily,
        planned_date=planned_date if not is_daily else None,
    )
    return RedirectResponse(url="/", status_code=303)


@router.post("/toggle/{task_id}")
def toggle(task_id: str):
    toggle_task(task_id)
    return RedirectResponse(url="/", status_code=303)


@router.post("/toggle-daily/{task_id}")
def toggle_daily_route(task_id: str):
    toggle_daily(task_id)
    return RedirectResponse(url="/", status_code=303)


@router.post("/delete/{task_id}")
def delete(task_id: str):
    delete_task(task_id)
    return RedirectResponse(url="/", status_code=303)
