from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from app.database import Base


class Role(Base):

    __tablename__ = "rol"
    __table_args__ = {"schema": "bienestar"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column("nombre",String(50), nullable=False)

    users = relationship(
        "User",
        back_populates="role"
    )