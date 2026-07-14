from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Feedback(Base):
    __tablename__ = "retroalimentacion"
    __table_args__ = {"schema": "bienestar"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column("usuario_id", Integer, ForeignKey("bienestar.usuario.id", ondelete="CASCADE"), nullable=False)
    category = Column("categoria", String(50), nullable=False)
    message = Column("mensaje", Text, nullable=False)
    created_at = Column("fecha", TIMESTAMP, server_default=func.now())

    user = relationship("User")