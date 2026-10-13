import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base
import enum

class ProgressStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"

class Progress(Base):
    __tablename__ = "progress"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False)
    status = Column(Enum(ProgressStatus, native_enum=False), default=ProgressStatus.not_started, nullable=False)
    time_spent_seconds = Column(Integer, default=0)
    last_accessed_at = Column(DateTime, default=datetime.utcnow)
    mastery_score = Column(Float, nullable=True)

    user = relationship("User")
    lesson = relationship("Lesson")

    __table_args__ = (
        UniqueConstraint('user_id', 'lesson_id', name='uix_user_lesson_progress'),
    )
