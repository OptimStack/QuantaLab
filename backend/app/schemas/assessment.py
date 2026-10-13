from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID
from app.models.assessment import AssessmentType, QuestionType

class QuestionBase(BaseModel):
    prompt: str
    type: QuestionType
    options_json: Optional[Any] = None
    correct_answer: Optional[str] = None
    starter_code: Optional[str] = None

class QuestionResponse(QuestionBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    assessment_id: UUID

class AssessmentBase(BaseModel):
    title: str
    lesson_id: Optional[UUID] = None
    type: AssessmentType
    passing_score: float = 0.0

class AssessmentResponse(AssessmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    questions: List[QuestionResponse] = []

class SubmissionCreate(BaseModel):
    question_id: UUID
    answer_text: Optional[str] = None
    submitted_code: Optional[str] = None

class SubmissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    question_id: UUID
    answer_text: Optional[str] = None
    submitted_code: Optional[str] = None
    is_correct: Optional[bool] = None
    score: Optional[float] = None
    graded_at: Optional[datetime] = None
    sandbox_job_id: Optional[str] = None
