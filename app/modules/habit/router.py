from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.habit.schema import HabitResponse
from app.modules.habit.service import HabitService

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.get("", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    return HabitService.get_all(db)