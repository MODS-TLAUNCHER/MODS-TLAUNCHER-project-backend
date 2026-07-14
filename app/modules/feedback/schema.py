from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class FeedbackCategory(str, Enum):
    SUGERENCIA = "Sugerencia"
    REPORTE_ERROR = "Reporte de error"
    OTRO = "Otro"

class FeedbackCreate(BaseModel):
    category: FeedbackCategory
    message: str = Field(min_length=1, max_length=1000)

class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    category: str
    message: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)