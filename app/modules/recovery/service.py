from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.reminder.model import Reminder
from app.modules.reminder.repository import ReminderRepository
from app.modules.reminder.schema import ReminderCreate, ReminderUpdate


class ReminderService:

    @staticmethod
    def get_mine(db: Session, user_id: int):
        return ReminderRepository.get_by_user(db, user_id)

    @staticmethod
    def _get_owned_or_404(db: Session, user_id: int, reminder_id: int) -> Reminder:
        reminder = ReminderRepository.get_by_id(db, reminder_id)
        if reminder is None or reminder.user_id != user_id:
            raise HTTPException(status_code=404, detail="Recordatorio no encontrado")
        return reminder

    @staticmethod
    def create(db: Session, user_id: int, payload: ReminderCreate) -> Reminder:
        reminder = Reminder(
            user_id=user_id,
            time=payload.time,
            message=payload.message,
            active=payload.active,
        )
        return ReminderRepository.create(db, reminder)

    @staticmethod
    def update(db: Session, user_id: int, reminder_id: int, payload: ReminderUpdate) -> Reminder:
        reminder = ReminderService._get_owned_or_404(db, user_id, reminder_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(reminder, field, value)
        return ReminderRepository.save(db, reminder)

    @staticmethod
    def delete(db: Session, user_id: int, reminder_id: int):
        reminder = ReminderService._get_owned_or_404(db, user_id, reminder_id)
        ReminderRepository.delete(db, reminder)
        return {"message": "Recordatorio eliminado"}