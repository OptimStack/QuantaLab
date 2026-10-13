import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db import Base
import enum

class SourceMode(str, enum.Enum):
    visual = "visual"
    code = "code"

class Circuit(Base):
    __tablename__ = "circuits"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=True)
    title = Column(String, nullable=False)
    gate_sequence_json = Column(JSON, default=list)
    source_mode = Column(Enum(SourceMode, native_enum=False), default=SourceMode.visual, nullable=False)
    source_code = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User")
    lesson = relationship("Lesson")
