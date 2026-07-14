from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Resource(Base):

    __tablename__ = "recurso_apoyo"
    __table_args__ = {"schema": "bienestar"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column("titulo", String(150), nullable=False)
    description = Column("descripcion", Text)
    type = Column("tipo", String(50))  
    url = Column("url", String(255))
    created_by = Column("creado_por", Integer, ForeignKey("bienestar.usuario.id"))

    creator = relationship("User")