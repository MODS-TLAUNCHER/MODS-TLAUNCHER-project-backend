from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.modules.report.schema import GenerateReportRequest, ReportResponse
from app.modules.report.service import ReportService
from app.modules.user.model import User

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/me/generate-weekly", response_model=ReportResponse, status_code=201)
def generate_my_weekly_report(
    payload: GenerateReportRequest = GenerateReportRequest(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ReportService.generate_weekly(db, current_user.id, payload.reference_date)

@router.get("/me", response_model=List[ReportResponse])
def get_my_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ReportService.get_mine(db, current_user.id)