from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.progress import ProgressStatus

class ProgressUpdate(BaseModel):
    status: ProgressStatus
    time_spent_seconds: int

class ProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    lesson_id: UUID
    status: ProgressStatus
    time_spent_seconds: int
    last_accessed_at: datetime
    mastery_score: Optional[float] = None
