from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Usuario

app = FastAPI()

@app.get("/hola")
def hola_mundo():

    db: Session = SessionLocal()

    usuario = db.query(Usuario).first()

    if usuario:
        return {
            "mensaje": "Hola Mundo Backend",
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre_completo,
                "correo": usuario.correo_institucional
            }
        }

    return {
        "mensaje": "Hola Mundo Backend",
        "usuario": None
    }