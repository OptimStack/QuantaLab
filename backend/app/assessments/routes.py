from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List

from app.db import get_db
from app.models.assessment import Assessment, Submission
from app.schemas.assessment import AssessmentResponse, SubmissionCreate, SubmissionResponse
from app.utils.decorators import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/lesson/{lesson_id}", response_model=List[AssessmentResponse])
async def get_lesson_assessments(lesson_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Assessment)
        .options(selectinload(Assessment.questions))
        .where(Assessment.lesson_id == lesson_id)
    )
    return result.scalars().all()

@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(assessment_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Assessment)
        .options(selectinload(Assessment.questions))
        .where(Assessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment

@router.post("/{assessment_id}/submit", response_model=SubmissionResponse)
async def submit_assessment(
    assessment_id: UUID,
    submission_in: SubmissionCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_sub = Submission(
        user_id=current_user.id,
        question_id=submission_in.question_id,
        answer_text=submission_in.answer_text,
        submitted_code=submission_in.submitted_code
    )
    db.add(new_sub)
    await db.commit()
    await db.refresh(new_sub)
    
    from app.assessments.tasks import grade_submission_sync
    background_tasks.add_task(grade_submission_sync, str(new_sub.id))
    
    return new_sub
