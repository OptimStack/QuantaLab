from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID

class LessonBase(BaseModel):
    title: str
    content_markdown: str
    concept_tags: List[str] = []
    order_index: int = 0
    estimated_minutes: int = 10

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    module_id: UUID

class ModuleBase(BaseModel):
    title: str
    order_index: int = 0

class ModuleCreate(ModuleBase):
    pass

class ModuleResponse(ModuleBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    course_id: UUID
    lessons: List[LessonResponse] = []

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    order_index: int = 0

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    modules: List[ModuleResponse] = []
