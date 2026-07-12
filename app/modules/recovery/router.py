from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.modules.reminder.schema import ReminderCreate, ReminderResponse, ReminderUpdate
from app.modules.reminder.service import ReminderService
from app.modules.user.model import User

router = APIRouter(prefix="/reminders", tags=["Reminders"])

@router.get("/me", response_model=List[ReminderResponse])
def get_my_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ReminderService.get_mine(db, current_user.id)

@router.post("/me", response_model=ReminderResponse, status_code=201)
def create_my_reminder(
    payload: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ReminderService.create(db, current_user.id, payload)

@router.patch("/me/{reminder_id}", response_model=ReminderResponse)
def update_my_reminder(
    reminder_id: int,
    payload: ReminderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ReminderService.update(db, current_user.id, reminder_id, payload)

@router.delete("/me/{reminder_id}")
def delete_my_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ReminderService.delete(db, current_user.id, reminder_id)