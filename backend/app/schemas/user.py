from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.user import UserRole

try:
    import email_validator
    from pydantic import EmailStr
except ImportError:
    EmailStr = str

class UserBase(BaseModel):
    name: str
    email: EmailStr
    institution: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.student

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    role: UserRole
    created_at: datetime
    updated_at: datetime
