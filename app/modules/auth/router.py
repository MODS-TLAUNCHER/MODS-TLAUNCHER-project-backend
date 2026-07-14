from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.modules.auth.schema import GoogleLoginRequest, PasswordLoginRequest, TokenResponse
from app.modules.auth.service import AuthService
from app.modules.user.model import User
from app.modules.user.schema import UserResponse
 
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/google", response_model=TokenResponse)
def login_with_google(payload: GoogleLoginRequest,db: Session = Depends(get_db)):
    return AuthService.login_with_google(db, payload.id_token)

@router.post("/login", response_model=TokenResponse)
def login_with_password(
    payload: PasswordLoginRequest,
    db: Session = Depends(get_db),
):
    return AuthService.login_with_password(db, payload.email, payload.password)

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user