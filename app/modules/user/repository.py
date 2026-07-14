from sqlalchemy.orm import Session
from app.modules.user.model import User


class UserRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_by_id(db: Session,user_id: int):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_institutional_email(db: Session,email: str):
        return (
            db.query(User)
            .filter(User.institutional_email == email)
            .first()
        )

    @staticmethod
    def get_by_google_sub(db: Session,google_sub: str):
        return (
            db.query(User)
            .filter(User.google_sub == google_sub)
            .first()
        )

    @staticmethod
    def get_by_alternative_email(db: Session,email: str):
        return (
            db.query(User)
            .filter(User.alternative_email == email)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        user: User
    ):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update(db: Session,user: User):
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(
        db: Session,
        user: User
    ):
        db.delete(user)
        db.commit()