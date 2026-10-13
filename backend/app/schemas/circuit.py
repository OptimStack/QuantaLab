from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID
from app.models.circuit import SourceMode

class CircuitBase(BaseModel):
    title: str
    lesson_id: Optional[UUID] = None
    gate_sequence_json: List[Any] = []
    source_mode: SourceMode = SourceMode.visual
    source_code: Optional[str] = None

class CircuitCreate(CircuitBase):
    pass

class CircuitUpdate(CircuitBase):
    pass

class CircuitResponse(CircuitBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
