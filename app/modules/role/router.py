from fastapi import APIRouter, Depends
from app.database import SessionLocal
from typing import List
from app.core.dependencies import require_admin
from app.modules.role.service import RoleService
from app.modules.role.schema import RoleCreate
from app.modules.role.schema import RoleResponse
from app.modules.user.model import User

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
def create_role(rol: RoleCreate,admin: User = Depends(require_admin)):

    db = SessionLocal()

    try:
        return RoleService.create(
            db,
            rol.nombre
        )

    finally:
        db.close()