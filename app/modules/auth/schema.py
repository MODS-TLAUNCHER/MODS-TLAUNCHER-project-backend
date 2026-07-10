from pydantic import BaseModel

from app.modules.user.schema import UserResponse


class GoogleLoginRequest(BaseModel):
    id_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    is_new_user: bool
    profile_incomplete: bool
    user: UserResponse