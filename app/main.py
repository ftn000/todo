from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routes import tasks, focus
from app.api.dependencies import get_daily_service
from app.services.task_service import TaskService
from app.api.dependencies import get_task_service
from app.utils.dates import today_iso
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine


app = FastAPI()

templates = Jinja2Templates(directory=Path(__file__).resolve().parents[1] / "templates")
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(tasks.router)
app.include_router(focus.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    get_daily_service().reset_if_needed()


@app.get("/", response_class=HTMLResponse)
def index(request: Request, service: TaskService = Depends(get_task_service)):
    groups = service.get_grouped_tasks()
    focus_task = service.get_focus_task()

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
            "focus_task": focus_task,
        },
    )
