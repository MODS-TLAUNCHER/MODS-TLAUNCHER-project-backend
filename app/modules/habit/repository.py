from sqlalchemy.orm import Session
from app.modules.habit.model import Habit

class HabitRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Habit).all()

    @staticmethod
    def get_by_id(db: Session, habit_id: int):
        return db.query(Habit).filter(Habit.id == habit_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(Habit).filter(Habit.name == name).first()

    @staticmethod
    def create(db: Session, habit: Habit):
        db.add(habit)
        db.commit()
        db.refresh(habit)
        return habit