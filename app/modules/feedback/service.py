from datetime import date as date_type
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.feedback.model import Feedback
from app.modules.feedback.repository import FeedbackRepository
from app.modules.feedback.schema import FeedbackCreate

class FeedbackService:

    @staticmethod
    def create(db: Session, user_id: int, payload: FeedbackCreate) -> Feedback:
        if FeedbackRepository.exists_for_user_on_date(db, user_id, date_type.today()):
            raise HTTPException(
                status_code=409,
                detail="Ya enviaste una retroalimentación hoy. Solo se permite una por día."
            )
        feedback = Feedback(
            user_id=user_id,
            category=payload.category.value,
            message=payload.message,
        )
        return FeedbackRepository.create(db, feedback)

    @staticmethod
    def get_mine(db: Session, user_id: int):
        return FeedbackRepository.get_by_user(db, user_id)

    @staticmethod
    def get_all(db: Session):
        return FeedbackRepository.get_all(db)