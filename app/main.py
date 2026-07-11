from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionLocal
from app.core.dependencies import get_db
from app.modules.role.router import router as role_router
from app.modules.user.router import router as user_router
from app.modules.auth.router import router as auth_router

app = FastAPI(
    title="biUNestar API",
    version="1.0.0"
)

app.include_router(role_router)
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
def start():
    return {
        "mensaje": "Bienvenido a biUNestar"
    }


@app.get("/health/db")
def check_db():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"estado": "Conexión exitosa"}
    finally:
        db.close()

