from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func

from app.db.database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    father_name = Column(String, nullable=True)
    roll_no = Column(String, nullable=True, unique=True, index=True)
    section = Column(String, nullable=True)
    semester = Column(Integer, nullable=True)
    is_ticket_used = Column(Boolean, default=False)
    status = Column(String, default="pending")
    entered_time = Column(DateTime(timezone=True), nullable=True)
    is_applied = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
