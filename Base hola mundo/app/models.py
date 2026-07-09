from sqlalchemy import Column, Integer, String
from app.database import Base

class Usuario(Base):

    __tablename__ = "usuario"
    __table_args__ = {"schema": "bienestar"}

    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String)
    correo_institucional = Column(String)