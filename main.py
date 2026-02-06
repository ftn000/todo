from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from services import get_grouped_tasks, add_task, toggle_task, delete_task, toggle_daily, get_focus_task
from daily import reset_daily_tasks
from focus import set_focus, clear_focus
from utils.dates import today_iso

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    groups = get_grouped_tasks()
    focus_task = get_focus_task()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "today": today_iso(),
            "daily_tasks": groups["daily"],
            "active_tasks": groups["active"],
            "future_tasks": groups["future"],
            "overdue_tasks": groups["overdue"],
            "done_tasks": groups["done"],
            "focus_task": focus_task
        }
    )


@app.on_event("startup")
def startup():
    reset_daily_tasks()


@app.post("/add")
def create_task(
        text_name: str = Form(..., alias="text-name"),
        text_description: str = Form("", alias="text-description"),
        is_daily: bool = Form(False, alias="is-daily"),
        planned_date: str | None = Form(None, alias="planned-date")
):
    add_task(
        text_name=text_name,
        text_description=text_description,
        is_daily=is_daily,
        planned_date=planned_date if not is_daily else None
    )
    return RedirectResponse(url="/", status_code=303)


@app.post("/toggle/{task_id}")
def toggle(task_id: str):
    toggle_task(task_id)
    return RedirectResponse(url="/", status_code=303)


@app.post("/toggle-daily/{task_id}")
def toggle_daily_route(task_id: str):
    toggle_daily(task_id)
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{task_id}")
def delete(task_id: str):
    delete_task(task_id)
    return RedirectResponse(url="/", status_code=303)


@app.post("/focus/{task_id}")
def set_focus_route(task_id: str):
    set_focus(task_id)
    return RedirectResponse(url="/", status_code=303)


@app.post("/focus/clear")
def clear_focus_route():
    clear_focus()
    return RedirectResponse(url="/", status_code=303)