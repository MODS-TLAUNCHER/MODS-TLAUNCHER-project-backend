from datetime import date as date_type
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class Mood(str, Enum):
    ALEGRE = "Alegre"
    TRANQUILO = "Tranquilo"
    MOTIVADO = "Motivado"
    CANSADO = "Cansado"
    ESTRESADO = "Estresado"
    TRISTE = "Triste"
    ANSIOSO = "Ansioso"
    NEUTRAL = "Neutral"


class DailyRecordCreate(BaseModel):
    date: date_type | None = None
    sleep_hours: int = Field(ge=0, le=24)
    water_intake: int = Field(ge=0)
    activity_minutes: int = Field(ge=0)

    mood: Mood
    comment: str | None = Field(default=None, max_length=500)


class DailyRecordResponse(BaseModel):
    id: int
    user_id: int
    date: date_type
    mood: str | None = None
    comment: str | None = None
    sleep_hours: int
    water_intake: int
    activity_minutes: int
    model_config = ConfigDict(from_attributes=True)


class WeeklyAveragesResponse(BaseModel):
    user_id: int
    start_date: date_type
    end_date: date_type
    days_logged: int
    avg_sleep_hours: float | None = None
    avg_water_intake: float | None = None
    avg_activity_minutes: float | None = None