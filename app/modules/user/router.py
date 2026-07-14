from typing import List
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db,get_current_user,require_admin
from app.modules.user.model import User
from app.modules.user.schema import UserCreate
from app.modules.user.schema import UserResponse
from app.modules.user.schema import UserUpdate
from app.modules.user.service import UserService

router = APIRouter(prefix="/users",tags=["Users"])

@router.get("",response_model=List[UserResponse])
def get_users(admin:User=Depends(require_admin), db: Session = Depends(get_db)):
    return UserService.get_all(db)

@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id: int,current_user :User=Depends(get_current_user) ,db: Session = Depends(get_db)):
    return UserService.get_by_id(
        db,
        user_id
    )

@router.get("/by-email/{institutional_email}",response_model=UserResponse)
def get_user_by_email(institutional_email: str,current_user:User=Depends(get_current_user),db: Session = Depends(get_db)):
    return UserService.get_by_institutional_email(
        db,
        institutional_email
    )

@router.post("",response_model=UserResponse,status_code=201)
def create_user(user: UserCreate,admin:User=Depends(require_admin),db: Session = Depends(get_db)):
    return UserService.create(
        db,
        user
    )

@router.patch("/{user_id}",response_model=UserResponse)
def update_user(user_id: int,user: UserUpdate,current_user:User=Depends(get_current_user),db: Session = Depends(get_db)):
    is_admin=current_user.role and current_user.role.name == "Administrador"
    if current_user.id!=user_id and not is_admin:
        raise HTTPException(status_code=403, detail="Solo puedes editar tu propio perfil")
    return UserService.update(
        db,
        user_id,
        user
    )

@router.delete("/{user_id}")
def delete_user(user_id: int,admin:User=Depends(require_admin),db: Session = Depends(get_db)):
    return UserService.delete(
        db,
        user_id
    )