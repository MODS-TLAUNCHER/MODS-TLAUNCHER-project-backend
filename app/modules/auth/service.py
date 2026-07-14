from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_google_id_token, verify_password
from app.modules.role.model import Role
from app.modules.role.repository import RoleRepository
from app.modules.user.model import User
from app.modules.user.repository import UserRepository

DEFAULT_ROLE_NAME = "Estudiante"


class AuthService:

    @staticmethod
    def _get_or_create_default_role(db: Session) -> Role:
        role = RoleRepository.get_by_name(db, DEFAULT_ROLE_NAME)
        if role is None:
            role = RoleRepository.create(db, Role(name=DEFAULT_ROLE_NAME))
        return role

    @staticmethod
    def _is_domain_allowed(email: str) -> bool:
        domain = email.rsplit("@", 1)[-1].lower()
        return domain in settings.allowed_domains_list

    @staticmethod
    def _issue_session(user: User, is_new_user: bool = False) -> dict:
        profile_incomplete = not (user.career and user.goal)

        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={"email": user.institutional_email, "role_id": user.role_id}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "is_new_user": is_new_user,
            "profile_incomplete": profile_incomplete,
            "user": user,
        }

    @staticmethod
    def login_with_google(db: Session, id_token: str):
        try:
            payload = verify_google_id_token(id_token)
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Token de Google inválido o expirado"
            )

        if not payload.get("email_verified", False):
            raise HTTPException(
                status_code=401,
                detail="El correo de Google no está verificado"
            )

        email = payload["email"].strip().lower()
        google_sub = payload["sub"]
        full_name = payload.get("name") or email.split("@")[0]

        if not AuthService._is_domain_allowed(email):
            raise HTTPException(
                status_code=403,
                detail=(
                    "Debes iniciar sesión con tu correo institucional "
                    f"({', '.join(settings.allowed_domains_list)})"
                )
            )

        user = UserRepository.get_by_google_sub(db, google_sub)
        is_new_user = False
        if user is None:
            user = UserRepository.get_by_institutional_email(db, email)
        if user is None:
            role = AuthService._get_or_create_default_role(db)
            user = User(
                full_name=full_name,
                institutional_email=email,
                google_sub=google_sub,
                is_verified=True,
                active=True,
                role_id=role.id,
                credits=0,
            )
            user = UserRepository.create(db, user)
            is_new_user = True
        else:
            if not user.active:
                raise HTTPException(
                    status_code=403,
                    detail="Esta cuenta ha sido desactivada por un administrador"
                )
            user.google_sub = google_sub
            user.is_verified = True
            user = UserRepository.update(db, user)
        return AuthService._issue_session(user, is_new_user)

    @staticmethod
    def login_with_password(db: Session, email: str, password: str):
        email = email.strip().lower()
        user = UserRepository.get_by_alternative_email(db, email)
        invalid_credentials = HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

        if user is None or not user.password_hash:
            raise invalid_credentials

        if not verify_password(password, user.password_hash):
            raise invalid_credentials

        if not user.active:
            raise HTTPException(status_code=403, detail="Esta cuenta ha sido desactivada por un administrador")

        return AuthService._issue_session(user, is_new_user=False)