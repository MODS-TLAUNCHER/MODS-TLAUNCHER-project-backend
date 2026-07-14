from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.user.model import User
from app.modules.user.repository import UserRepository
from app.modules.user.schema import UserCreate
from app.modules.user.schema import UserUpdate


class UserService:

    @staticmethod
    def get_all(db: Session):
        return UserRepository.get_all(db)

    @staticmethod
    def get_by_id(db: Session,user_id: int):
        user = UserRepository.get_by_id(
            db,
            user_id
        )
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return user
    
    @staticmethod
    def get_by_institutional_email(db: Session,institutional_email: str):
        user = UserRepository.get_by_institutional_email(
            db,
            institutional_email
        )
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return user

    @staticmethod
    def create(db: Session,user_data: UserCreate):
        existing_user = UserRepository.get_by_institutional_email(
            db,
            user_data.institutional_email
        )
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        user = User(
            full_name=user_data.full_name,
            institutional_email=user_data.institutional_email,
            alternative_email=user_data.alternative_email,
            password_hash=hash_password(
                user_data.password
            )if user_data.password else None,
            career=user_data.career,
            credits=user_data.credits,
            goal=user_data.goal,
            stress_level=user_data.stress_level,
            active=user_data.active,
            role_id=user_data.role_id
        )
        return UserRepository.create(
            db,
            user
        )

    @staticmethod
    def update(db: Session,user_id: int,user_data: UserUpdate):

        user = UserRepository.get_by_id(db,user_id)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        update_data = user_data.model_dump(exclude_unset=True)
        if "password" in update_data:

            user.password_hash = hash_password(
                update_data.pop("password")
            )
        for field, value in update_data.items():
            setattr(user,field,value)
        return UserRepository.update(db, user)

    @staticmethod
    def delete(db: Session,user_id: int):
        user = UserRepository.get_by_id(
            db,
            user_id
        )
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        UserRepository.delete(
            db,
            user
        )
        return {
            "message": "User deleted successfully"
        }