from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):

    __tablename__ = "usuario"
    __table_args__ = {"schema": "bienestar"}

    id = Column(Integer,primary_key=True,index=True)

    full_name = Column("nombre_completo",String(150),nullable=False)

    institutional_email=Column(
        "correo_institucional",
        String(150),
        unique=True,
        nullable=False
    )

    alternative_email = Column("correo_alternativo",String(150))
    password_hash = Column(String(255),nullable=False)
    carrer= Column("carrera",String(100))
    credits = Column("creditos",Integer,default=0)
    goal = Column("meta",Text)
    stress_level = Column("nivel_estres",Integer)
    active = Column("activo",Boolean,default=True)
    created_at = Column(
        "creado_en",
        TIMESTAMP,
        server_default=func.now()
    )

    role_id = Column(
        "rol_id",
        Integer,
        ForeignKey("bienestar.rol.id")
    )

    role = relationship(
        "Role",
        back_populates="users"
    )