from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db, require_admin
from app.modules.feedback.schema import FeedbackCreate, FeedbackResponse
from app.modules.feedback.service import FeedbackService
from app.modules.user.model import User

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/me", response_model=FeedbackResponse, status_code=201)
def send_my_feedback(
    payload: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return FeedbackService.create(db, current_user.id, payload)

@router.get("/me", response_model=List[FeedbackResponse])
def get_my_feedback(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return FeedbackService.get_mine(db, current_user.id)

@router.get("", response_model=List[FeedbackResponse])
def get_all_feedback(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return FeedbackService.get_all(db)