from datetime import date as date_type
from sqlalchemy.orm import Session
from app.modules.daily_record.service import DailyRecordService
from app.modules.report.model import Report
from app.modules.report.repository import ReportRepository

class ReportService:

    @staticmethod
    def generate_weekly(db: Session, user_id: int, reference_date: date_type | None = None) -> Report:
        
        averages = DailyRecordService.get_weekly_averages(db, user_id, reference_date)
        iso_year, iso_week, _ = averages.start_date.isocalendar()

        report = ReportRepository.get_by_user_week_year(db, user_id, iso_week, iso_year)

        if report is None:
            report = Report(
                user_id=user_id,
                week=iso_week,
                year=iso_year,
                avg_sleep_hours=averages.avg_sleep_hours,
                avg_water_intake=averages.avg_water_intake,
                avg_activity_minutes=averages.avg_activity_minutes,
            )
            return ReportRepository.create(db, report)

        report.avg_sleep_hours = averages.avg_sleep_hours
        report.avg_water_intake = averages.avg_water_intake
        report.avg_activity_minutes = averages.avg_activity_minutes
        return ReportRepository.save(db, report)

    @staticmethod
    def get_mine(db: Session, user_id: int):
        return ReportRepository.get_by_user(db, user_id)