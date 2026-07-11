from datetime import date as date_type
from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.daily_record.model import DailyRecord, HabitRecord
from app.modules.daily_record.repository import DailyRecordRepository
from app.modules.daily_record.schema import DailyRecordCreate, DailyRecordResponse, WeeklyAveragesResponse
from app.modules.habit.model import HABIT_ACTIVITY, HABIT_SLEEP, HABIT_WATER
from app.modules.habit.service import HabitService

class DailyRecordService:

    @staticmethod
    def _to_response(record: DailyRecord) -> DailyRecordResponse:
        values = {hr.habit.name: hr.value for hr in record.habit_records}
        return DailyRecordResponse(
            id=record.id,
            user_id=record.user_id,
            date=record.date,
            mood=record.mood,
            comment=record.comment,
            sleep_hours=values.get(HABIT_SLEEP, 0),
            water_intake=values.get(HABIT_WATER, 0),
            activity_minutes=values.get(HABIT_ACTIVITY, 0),
        )

    @staticmethod
    def upsert(db: Session, user_id: int, payload: DailyRecordCreate) -> DailyRecordResponse:
        record_date = payload.date or date_type.today()

        if record_date > date_type.today():
            raise HTTPException(status_code=400, detail="No se pueden registrar hábitos de una fecha futura")

        default_habits = HabitService.get_or_create_defaults(db)
        target_values = {
            default_habits[HABIT_SLEEP].id: payload.sleep_hours,
            default_habits[HABIT_WATER].id: payload.water_intake,
            default_habits[HABIT_ACTIVITY].id: payload.activity_minutes,
        }

        record = DailyRecordRepository.get_by_user_and_date(db, user_id, record_date)

        if record is None:
            record = DailyRecord(
                user_id=user_id,
                date=record_date,
                mood=payload.mood.value,
                comment=payload.comment,
                habit_records=[
                    HabitRecord(habit_id=habit_id, value=value)
                    for habit_id, value in target_values.items()
                ],
            )
            record = DailyRecordRepository.create(db, record)
        else:
            record.mood = payload.mood.value
            record.comment = payload.comment

            existing_by_habit = {hr.habit_id: hr for hr in record.habit_records}
            for habit_id, value in target_values.items():
                if habit_id in existing_by_habit:
                    existing_by_habit[habit_id].value = value
                else:
                    record.habit_records.append(HabitRecord(habit_id=habit_id, value=value))

            record = DailyRecordRepository.save(db, record)
        record = DailyRecordRepository.get_by_id(db, record.id)
        return DailyRecordService._to_response(record)

    @staticmethod
    def get_today(db: Session, user_id: int) -> DailyRecordResponse | None:
        record = DailyRecordRepository.get_by_user_and_date(db, user_id, date_type.today())
        return DailyRecordService._to_response(record) if record else None

    @staticmethod
    def get_history(db: Session, user_id: int, start_date: date_type, end_date: date_type) -> list[DailyRecordResponse]:
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="start_date no puede ser posterior a end_date")

        records = DailyRecordRepository.get_range(db, user_id, start_date, end_date)
        return [DailyRecordService._to_response(r) for r in records]

    @staticmethod
    def get_weekly_averages(db: Session, user_id: int, reference_date: date_type | None = None) -> WeeklyAveragesResponse:
        reference_date = reference_date or date_type.today()
        start_date = reference_date - timedelta(days=reference_date.weekday()) 
        end_date = start_date + timedelta(days=6)  

        records = DailyRecordRepository.get_range(db, user_id, start_date, end_date)
        responses = [DailyRecordService._to_response(r) for r in records]

        days_logged = len(responses)

        def _avg(values: list[int]) -> float | None:
            return round(sum(values) / len(values), 2) if values else None

        return WeeklyAveragesResponse(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            days_logged=days_logged,
            avg_sleep_hours=_avg([r.sleep_hours for r in responses]),
            avg_water_intake=_avg([r.water_intake for r in responses]),
            avg_activity_minutes=_avg([r.activity_minutes for r in responses]),
        )