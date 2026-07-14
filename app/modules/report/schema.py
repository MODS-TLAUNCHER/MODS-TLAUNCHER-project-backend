from datetime import date as date_type
from pydantic import BaseModel, ConfigDict

class ReportResponse(BaseModel):
    id: int
    user_id: int
    week: int
    year: int
    avg_sleep_hours: float | None = None
    avg_water_intake: float | None = None
    avg_activity_minutes: float | None = None
    model_config = ConfigDict(from_attributes=True)

class GenerateReportRequest(BaseModel):
    reference_date: date_type | None = None