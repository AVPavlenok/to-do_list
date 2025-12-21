from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declared_attr

from src.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


class User(BaseModel):
    name = Column(String(255), nullable=False)
    login = Column(String(20), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    tasks = relationship("Task", back_populates='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.name}"


class Task(BaseModel):
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task = Column(String(255), nullable=False)
    is_complete = Column(Boolean, default=False)

    user = relationship("User", back_populates="tasks")

