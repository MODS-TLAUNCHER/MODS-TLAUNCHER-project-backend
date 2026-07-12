from sqlalchemy import Column, Float, ForeignKey, Integer, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Report(Base):
    __tablename__ = "reporte"
    __table_args__ = (
        UniqueConstraint("usuario_id", "semana", "anio", name="uq_reporte_usuario_semana_anio"),
        {"schema": "bienestar"},
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column("usuario_id", Integer, ForeignKey("bienestar.usuario.id", ondelete="CASCADE"), nullable=False)
    week = Column("semana", Integer, nullable=False)
    year = Column("anio", Integer, nullable=False)
    avg_sleep_hours = Column("promedio_sueno", Float)
    avg_water_intake = Column("promedio_agua", Float)
    avg_activity_minutes = Column("promedio_actividad", Float)
    created_at = Column("creado_en", TIMESTAMP, server_default=func.now())

    user = relationship("User")