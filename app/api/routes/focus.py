from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.domain.exceptions import DomainError
from app.services.focus_service import FocusService
from app.api.dependencies import get_focus_service

router = APIRouter()

@router.post("/focus/clear")
def clear_focus_route(service: FocusService = Depends(get_focus_service)):
    service.clear_focus()
    return RedirectResponse(url="/", status_code=303)

@router.post("/focus/{task_id}")
def set_focus_route(task_id: str, service: FocusService = Depends(get_focus_service)):
    try:
        service.set_focus(task_id)
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return RedirectResponse(url="/", status_code=303)