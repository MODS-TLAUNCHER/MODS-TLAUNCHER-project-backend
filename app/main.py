from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionLocal
from app.core.dependencies import get_db
from app.modules.role.router import router as role_router
from app.modules.user.router import router as user_router
from app.modules.auth.router import router as auth_router
from app.modules.habit.router import router as habit_router
from app.modules.daily_record.router import router as daily_record_router
from app.modules.reminder.router import router as reminder_router
from app.modules.report.router import router as report_router
from app.modules.resource.router import router as resource_router

from app.modules.habit.service import HabitService

app = FastAPI(
    title="biUNestar API",
    version="1.0.0"
)

app.include_router(role_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(habit_router)
app.include_router(daily_record_router)
app.include_router(reminder_router)
app.include_router(report_router)
app.include_router(resource_router)

@app.get("/")
def start():
    return {
        "mensaje": "Bienvenido a biUNestar"
    }

@app.on_event("startup")
def seed_default_habits():
    db = SessionLocal()
    try:
        HabitService.get_or_create_defaults(db)
    except Exception:
        pass
    finally:
        db.close()

@app.get("/health/db")
def check_db():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"estado": "Conexión exitosa"}
    finally:
        db.close()

