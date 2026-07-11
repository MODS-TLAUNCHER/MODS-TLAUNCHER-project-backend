from pydantic import BaseModel, ConfigDict


class HabitResponse(BaseModel):
    id: int
    name: str
    unit: str | None = None
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)