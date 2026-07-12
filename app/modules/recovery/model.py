from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship
from app.database import Base


class Reminder(Base):
    __tablename__ = "recordatorio"
    __table_args__ = {"schema": "bienestar"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column("usuario_id", Integer, ForeignKey("bienestar.usuario.id", ondelete="CASCADE"), nullable=False)
    time = Column("hora", Time, nullable=False)
    message = Column("mensaje", String(255))
    active = Column("activo", Boolean, default=True)

    user = relationship("User")