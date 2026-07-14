from datetime import date as date_type
from sqlalchemy.orm import Session, joinedload
from app.modules.daily_record.model import DailyRecord, HabitRecord

class DailyRecordRepository:

    @staticmethod
    def get_by_user_and_date(db: Session, user_id: int, record_date: date_type):
        return (
            db.query(DailyRecord)
            .options(joinedload(DailyRecord.habit_records).joinedload(HabitRecord.habit))
            .filter(DailyRecord.user_id == user_id, DailyRecord.date == record_date)
            .first()
        )

    @staticmethod
    def get_by_id(db: Session, record_id: int):
        return (
            db.query(DailyRecord)
            .options(joinedload(DailyRecord.habit_records).joinedload(HabitRecord.habit))
            .filter(DailyRecord.id == record_id)
            .first()
        )

    @staticmethod
    def get_range(db: Session, user_id: int, start_date: date_type, end_date: date_type):
        return (
            db.query(DailyRecord)
            .options(joinedload(DailyRecord.habit_records).joinedload(HabitRecord.habit))
            .filter(
                DailyRecord.user_id == user_id,
                DailyRecord.date >= start_date,
                DailyRecord.date <= end_date,
            )
            .order_by(DailyRecord.date.asc())
            .all()
        )

    @staticmethod
    def create(db: Session, daily_record: DailyRecord) -> DailyRecord:
        db.add(daily_record)
        db.commit()
        db.refresh(daily_record)
        return daily_record

    @staticmethod
    def save(db: Session, daily_record: DailyRecord) -> DailyRecord:
        db.commit()
        db.refresh(daily_record)
        return daily_record

    @staticmethod
    def delete(db: Session, daily_record: DailyRecord):
        db.delete(daily_record)
        db.commit()