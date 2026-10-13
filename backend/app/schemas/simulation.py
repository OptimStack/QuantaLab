from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime
from uuid import UUID
from app.models.simulation_job import JobBackend, JobStatus

class SimulationJobCreate(BaseModel):
    circuit_id: UUID
    backend: JobBackend

class SimulationJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    circuit_id: UUID
    requested_by: UUID
    backend: JobBackend
    status: JobStatus
    result_json: Optional[Any] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
