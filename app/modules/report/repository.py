from sqlalchemy.orm import Session
from app.modules.report.model import Report

class ReportRepository:

    @staticmethod
    def get_by_user_week_year(db: Session, user_id: int, week: int, year: int):
        return (
            db.query(Report)
            .filter(Report.user_id == user_id, Report.week == week, Report.year == year)
            .first()
        )

    @staticmethod
    def get_by_id(db: Session, report_id: int):
        return db.query(Report).filter(Report.id == report_id).first()

    @staticmethod
    def get_by_user(db: Session, user_id: int):
        return (
            db.query(Report)
            .filter(Report.user_id == user_id)
            .order_by(Report.year.desc(), Report.week.desc())
            .all()
        )

    @staticmethod
    def create(db: Session, report: Report) -> Report:
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def save(db: Session, report: Report) -> Report:
        db.commit()
        db.refresh(report)
        return report