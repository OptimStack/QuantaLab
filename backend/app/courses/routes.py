from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID

from app.db import get_db
from app.models.course import Course, Module, Lesson
from app.schemas.course import CourseResponse, LessonResponse

router = APIRouter()

@router.get("", response_model=List[CourseResponse])
async def list_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).options(selectinload(Course.modules).selectinload(Module.lessons)).order_by(Course.order_index))
    courses = result.scalars().all()
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson
