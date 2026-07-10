from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.role.model import Role
from app.modules.role.repository import RoleRepository


class RoleService:

    @staticmethod
    def get_all(db: Session):
        return RoleRepository.get_all(db)

    @staticmethod
    def get_by_id(db: Session,role_id: int):

        role = RoleRepository.get_by_id(db,role_id)

        if role is None:
            raise HTTPException(
                status_code=404,
                detail="Role not found"
            )

        return role

    @staticmethod
    def create(db: Session,name: str):

        existing = RoleRepository.get_by_name(db,name)

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Role already exists"
            )

        role = Role(name=name)

        return RoleRepository.create(db,role)