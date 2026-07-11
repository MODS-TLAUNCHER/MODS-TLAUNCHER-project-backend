from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class DailyRecord(Base):
    __tablename__ = "registro_diario"
    __table_args__ = (
        UniqueConstraint("usuario_id", "fecha", name="uq_registro_usuario_fecha"),
        {"schema": "bienestar"},
    )
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column("usuario_id", Integer, ForeignKey("bienestar.usuario.id", ondelete="CASCADE"), nullable=False)
    date = Column("fecha", Date, nullable=False)
    mood = Column("estado_animo", String(50))
    comment = Column("comentario", String(500))
    created_at = Column("creado_en", TIMESTAMP, server_default=func.now())
    user = relationship("User")
    habit_records = relationship(
        "HabitRecord",
        back_populates="daily_record",
        cascade="all, delete-orphan"
    )

class HabitRecord(Base):
    __tablename__ = "registro_habito"
    __table_args__ = {"schema": "bienestar"}

    id = Column(Integer, primary_key=True, index=True)
    daily_record_id = Column(
        "registro_id",
        Integer,
        ForeignKey("bienestar.registro_diario.id", ondelete="CASCADE"),
        nullable=False
    )
    habit_id = Column("habito_id", Integer, ForeignKey("bienestar.habito.id"), nullable=False)
    value = Column("valor", Integer, nullable=False)

    daily_record = relationship("DailyRecord", back_populates="habit_records")
    habit = relationship("Habit", back_populates="records")