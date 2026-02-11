from dataclasses import dataclass
from typing import Optional
from datetime import date, timedelta

@dataclass
class Task:
    id: str
    text_name: str
    text_description: str

    done: bool = False
    is_daily: bool = False

    completed_count: int = 0
    streak: int = 0

    planned_date: Optional[str] = None
    last_completed_date: Optional[str] = None

    def mark_done(self, today: date) -> None:
        if self.done:
            return

        self.done = True
        self.completed_count += 1

        if self.is_daily:
            self.update_streak(today)

    def mark_undone(self) -> None:
        self.done = False

    def toggle_daily(self) -> None:
        self.is_daily = not self.is_daily
        if self.is_daily:
            self.planned_date = None

    def reset_daily(self) -> None:
        if self.is_daily:
            self.done = False

    def update_streak(self, today: date) -> None:
        if not self.last_completed_date:
            self.streak = 1
        else:
            last = date.fromisoformat(self.last_completed_date)

            if last == today:
                return
            elif last == today - timedelta(days=1):
                self.streak += 1
            else:
                self.streak = 1

        self.last_completed_date = today.isoformat()
