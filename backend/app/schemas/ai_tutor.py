from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.ai_tutor_session import RoleType, SessionMode

class AiTutorMessageBase(BaseModel):
    role: RoleType
    mode: SessionMode
    content: str

class AiTutorMessageResponse(AiTutorMessageBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    session_id: UUID
    created_at: datetime

class AiTutorSessionBase(BaseModel):
    lesson_id: Optional[UUID] = None
    circuit_id: Optional[UUID] = None

class AiTutorSessionResponse(AiTutorSessionBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    started_at: datetime
    messages: List[AiTutorMessageResponse] = []
