import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db import Base
import enum

class AssessmentType(str, enum.Enum):
    quiz = "quiz"
    coding_challenge = "coding_challenge"

class QuestionType(str, enum.Enum):
    mcq = "mcq"
    coding = "coding"

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=True)
    title = Column(String, nullable=False)
    type = Column(Enum(AssessmentType, native_enum=False), nullable=False)
    passing_score = Column(Float, default=0.0)

    lesson = relationship("Lesson")
    questions = relationship("Question", back_populates="assessment", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String(36), ForeignKey("assessments.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    type = Column(Enum(QuestionType, native_enum=False), nullable=False)
    options_json = Column(JSON, nullable=True)
    correct_answer = Column(String, nullable=True)
    starter_code = Column(Text, nullable=True)

    assessment = relationship("Assessment", back_populates="questions")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=False)
    answer_text = Column(Text, nullable=True)
    submitted_code = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    score = Column(Float, nullable=True)
    graded_at = Column(DateTime, nullable=True)
    sandbox_job_id = Column(String, nullable=True)

    user = relationship("User")
    question = relationship("Question")
