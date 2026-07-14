from sqlalchemy.orm import Session
from app.modules.reminder.model import Reminder


class ReminderRepository:

    @staticmethod
    def get_by_user(db: Session, user_id: int):
        return (
            db.query(Reminder)
            .filter(Reminder.user_id == user_id)
            .order_by(Reminder.time.asc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, reminder_id: int):
        return db.query(Reminder).filter(Reminder.id == reminder_id).first()

    @staticmethod
    def create(db: Session, reminder: Reminder) -> Reminder:
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        return reminder

    @staticmethod
    def save(db: Session, reminder: Reminder) -> Reminder:
        db.commit()
        db.refresh(reminder)
        return reminder

    @staticmethod
    def delete(db: Session, reminder: Reminder):
        db.delete(reminder)
        db.commit()