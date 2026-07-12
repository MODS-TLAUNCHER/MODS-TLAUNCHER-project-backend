from datetime import date as date_type, datetime, time
from sqlalchemy.orm import Session
from app.modules.feedback.model import Feedback

class FeedbackRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Feedback).order_by(Feedback.created_at.desc()).all()

    @staticmethod
    def get_by_id(db: Session, feedback_id: int):
        return db.query(Feedback).filter(Feedback.id == feedback_id).first()

    @staticmethod
    def get_by_user(db: Session, user_id: int):
        return (
            db.query(Feedback)
            .filter(Feedback.user_id == user_id)
            .order_by(Feedback.created_at.desc())
            .all()
        )

    @staticmethod
    def exists_for_user_on_date(db: Session, user_id: int, day: date_type) -> bool:
        day_start = datetime.combine(day, time.min)
        day_end = datetime.combine(day, time.max)
        return (
            db.query(Feedback)
            .filter(
                Feedback.user_id == user_id,
                Feedback.created_at >= day_start,
                Feedback.created_at <= day_end,
            )
            .first()
            is not None
        )

    @staticmethod
    def create(db: Session, feedback: Feedback) -> Feedback:
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        return feedback