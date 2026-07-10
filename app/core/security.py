from datetime import datetime, timedelta, timezone
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def verify_google_id_token(token: str) -> dict:
    payload = google_id_token.verify_oauth2_token(
        token,
        google_requests.Request(),
        settings.GOOGLE_CLIENT_ID
    )

    issuer = payload.get("iss")
    if issuer not in ("accounts.google.com", "https://accounts.google.com"):
        raise ValueError("Emisor de token inválido")

    return payload

def create_access_token(subject: str, extra_claims: dict | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    if extra_claims:
        to_encode.update(extra_claims)

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM]
    )