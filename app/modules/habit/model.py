from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
 
from app.database import Base
 
 
class Habit(Base):
    __tablename__ = "habito"
    __table_args__ = {"schema": "bienestar"}
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column("nombre", String(100), nullable=False, unique=True)
    unit = Column("unidad", String(50))
    description = Column("descripcion", Text)
 
    records = relationship("HabitRecord", back_populates="habit")
  
HABIT_SLEEP = "Sueño"
HABIT_WATER = "Agua"
HABIT_ACTIVITY = "Actividad física"