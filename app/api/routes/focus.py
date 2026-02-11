from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.focus_service import set_focus, clear_focus

router = APIRouter()

@router.post("/focus/clear")
def clear_focus_route():
    clear_focus()
    return RedirectResponse(url="/", status_code=303)

@router.post("/focus/{task_id}")
def set_focus_route(task_id: str):
    set_focus(task_id)
    return RedirectResponse(url="/", status_code=303)