from datetime import date as date_type
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.modules.daily_record.schema import (
    DailyRecordCreate,
    DailyRecordResponse,
    WeeklyAveragesResponse,
)
from app.modules.daily_record.service import DailyRecordService
from app.modules.user.model import User

router = APIRouter(prefix="/daily-records", tags=["Daily Records"])


@router.post("/me", response_model=DailyRecordResponse, status_code=201)
def upsert_my_daily_record(
    payload: DailyRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DailyRecordService.upsert(db, current_user.id, payload)

@router.get("/me/today", response_model=DailyRecordResponse)
def get_my_today_record(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = DailyRecordService.get_today(db, current_user.id)
    if record is None:
        raise HTTPException(status_code=404, detail="Aún no has registrado tus hábitos de hoy")
    return record

@router.get("/me", response_model=List[DailyRecordResponse])
def get_my_history(
    start_date: date_type = Query(..., description="Fecha inicial (YYYY-MM-DD)"),
    end_date: date_type = Query(..., description="Fecha final (YYYY-MM-DD)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DailyRecordService.get_history(db, current_user.id, start_date, end_date)

@router.get("/me/weekly-averages", response_model=WeeklyAveragesResponse)
def get_my_weekly_averages(
    reference_date: date_type | None = Query(
        default=None,
        description="Cualquier fecha dentro de la semana a promediar. Por defecto: hoy.",
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DailyRecordService.get_weekly_averages(db, current_user.id, reference_date)