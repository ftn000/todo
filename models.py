from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Task:
    id: str
    text_name: str
    text_description: str

    done: bool = False
    is_daily: bool = False

    #Счетчики
    completed_count: int = 0
    streak: int = 0

    #Даты
    planned_date: Optional[str] = None          #ISO: 2026-01-13
    last_completed_date: Optional[str] = None   #ISO