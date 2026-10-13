import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
import enum

class RoleType(str, enum.Enum):
    user = "user"
    assistant = "assistant"

class SessionMode(str, enum.Enum):
    explain = "explain"
    generate = "generate"
    debug = "debug"
    recommend = "recommend"

class AiTutorSession(Base):
    __tablename__ = "ai_tutor_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=True)
    circuit_id = Column(String(36), ForeignKey("circuits.id"), nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    messages = relationship("AiTutorMessage", back_populates="session", cascade="all, delete-orphan")

class AiTutorMessage(Base):
    __tablename__ = "ai_tutor_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("ai_tutor_sessions.id"), nullable=False)
    role = Column(Enum(RoleType, native_enum=False), nullable=False)
    mode = Column(Enum(SessionMode, native_enum=False), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("AiTutorSession", back_populates="messages")
