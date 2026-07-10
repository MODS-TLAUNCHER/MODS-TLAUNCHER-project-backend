from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.database import SessionLocal
from app.modules.user.model import User
from app.modules.user.repository import UserRepository


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


_bearer_scheme = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Credenciales inválidas o token expirado")

    user = UserRepository.get_by_id(db, user_id)
    if user is None or not user.active:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo")

    return user


def require_role(*allowed_role_ids: int):
    def _dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role_id not in allowed_role_ids:
            raise HTTPException(status_code=403, detail="No tienes permisos para esta acción")
        return current_user

    return _dependency