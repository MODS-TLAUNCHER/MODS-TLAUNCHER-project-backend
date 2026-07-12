from datetime import time as time_type
from pydantic import BaseModel, ConfigDict, Field


class ReminderCreate(BaseModel):
    time: time_type
    message: str | None = Field(default=None, max_length=255)
    active: bool = True

class ReminderUpdate(BaseModel):
    time: time_type | None = None
    message: str | None = Field(default=None, max_length=255)
    active: bool | None = None

class ReminderResponse(BaseModel):
    id: int
    user_id: int
    time: time_type
    message: str | None = None
    active: bool
    model_config = ConfigDict(from_attributes=True)