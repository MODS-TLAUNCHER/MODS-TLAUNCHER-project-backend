from pydantic import BaseModel,ConfigDict,EmailStr,Field


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
    password: str | None=Field(default=None,min_length=8)


class UserResponse(UserBase):
    id: int
    is_verified:bool
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):

    full_name: str | None = None
    alternative_email: EmailStr | None = None
    career: str | None = None
    credits: int | None = Field(default=None, ge=0)
    goal: str | None = None
    stress_level: int | None = Field(default=None, ge=1, le=5)
    active: bool | None = None
    password: str | None = Field(default=None, min_length=8)