import re
from pydantic import AliasPath, BaseModel,ConfigDict,EmailStr,Field,field_validator

_PASSWORD_SPECIALS = r"!@#$%^&*()_+\-=\[\]{};:,.?/|"
_PASSWORD_PATTERN = re.compile(
    rf"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[{_PASSWORD_SPECIALS}])[A-Za-z\d{_PASSWORD_SPECIALS}]{{8,20}}$"
)

def validate_password_policy(password: str) -> str:
    if not _PASSWORD_PATTERN.match(password):
        raise ValueError(
            "La contraseña debe tener entre 8 y 20 caracteres, e incluir al menos una "
            "mayúscula, una minúscula, un número y un carácter especial "
            "(! @ # $ % ^ & * ( ) _ + - = [ ] { } ; : , . ? / |), sin espacios."
        )
    return password

class UserBase(BaseModel):

    full_name: str
    institutional_email: EmailStr
    alternative_email: EmailStr | None = None
    career: str | None = None
    credits: int = 0
    goal: str | None = None
    stress_level: int | None = None
    active: bool = True
    role_id: int

class UserCreate(UserBase):
    password: str | None = None
    @field_validator("password")
    @classmethod
    def _check_password(cls, v):
        return validate_password_policy(v) if v else v

class UserResponse(UserBase):
    id: int
    is_verified: bool
    role_name: str | None = Field(default=None, validation_alias=AliasPath("role", "name"))
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserUpdate(BaseModel):

    full_name: str | None = None
    alternative_email: EmailStr | None = None
    career: str | None = None
    credits: int | None = Field(default=None, ge=0)
    goal: str | None = None
    stress_level: int | None = Field(default=None, ge=1, le=5)
    active: bool | None = None
    password: str | None = None
    @field_validator("password")
    @classmethod
    def _check_password(cls, v):
        return validate_password_policy(v) if v else v