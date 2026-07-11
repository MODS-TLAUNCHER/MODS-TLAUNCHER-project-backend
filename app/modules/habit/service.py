from sqlalchemy.orm import Session

from app.modules.habit.model import (
    HABIT_ACTIVITY,
    HABIT_SLEEP,
    HABIT_WATER,
    Habit,
)
from app.modules.habit.repository import HabitRepository

_DEFAULT_HABITS = {
    HABIT_SLEEP: "horas",
    HABIT_WATER: "vasos",
    HABIT_ACTIVITY: "minutos",
}


class HabitService:

    @staticmethod
    def get_all(db: Session):
        return HabitRepository.get_all(db)

    @staticmethod
    def get_or_create(db: Session, name: str, unit: str | None = None) -> Habit:
        habit = HabitRepository.get_by_name(db, name)
        if habit is None:
            habit = HabitRepository.create(db, Habit(name=name, unit=unit))
        return habit

    @staticmethod
    def get_or_create_defaults(db: Session) -> dict[str, Habit]:
        return {
            name: HabitService.get_or_create(db, name, unit)
            for name, unit in _DEFAULT_HABITS.items()
        }