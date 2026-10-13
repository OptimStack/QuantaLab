from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from .user import UserResponse

class InstructorCohortBase(BaseModel):
    name: str
    course_id: UUID

class InstructorCohortCreate(InstructorCohortBase):
    pass

class InstructorCohortResponse(InstructorCohortBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    instructor_id: UUID
    members: List[UserResponse] = []

class AddMembersRequest(BaseModel):
    user_ids: List[UUID]
