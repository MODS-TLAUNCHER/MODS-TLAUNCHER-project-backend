from fastapi import APIRouter
from app.database import SessionLocal
from typing import List
from app.modules.role.service import RoleService
from app.modules.role.schema import RoleCreate
from app.modules.role.schema import RoleResponse

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.get("",response_model=List[RoleResponse])
def list_roles():

    db = SessionLocal()

    try:
        return RoleService.get_all(db)

    finally:
        db.close()


@router.get("/{role_id}",response_model=RoleResponse)
def get_role(rol_id: int):

    db = SessionLocal()

    try:
        return RoleService.get_by_id(db,rol_id)

    finally:
        db.close()


@router.post("")
def create_role(rol: RoleCreate):

    db = SessionLocal()

    try:
        return RoleService.create(
            db,
            rol.nombre
        )

    finally:
        db.close()