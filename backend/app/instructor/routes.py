from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List

from app.db import get_db
from app.models.instructor_cohort import InstructorCohort
from app.models.user import User
from app.schemas.instructor import InstructorCohortCreate, InstructorCohortResponse, AddMembersRequest
from app.utils.decorators import get_current_user, role_required

router = APIRouter()

@router.get("/cohorts", response_model=List[InstructorCohortResponse])
async def list_cohorts(current_user: User = Depends(role_required("instructor", "admin")), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InstructorCohort)
        .options(selectinload(InstructorCohort.members))
        .where(InstructorCohort.instructor_id == current_user.id)
    )
    return result.scalars().all()

@router.post("/cohorts", response_model=InstructorCohortResponse)
async def create_cohort(cohort_in: InstructorCohortCreate, current_user: User = Depends(role_required("instructor", "admin")), db: AsyncSession = Depends(get_db)):
    new_cohort = InstructorCohort(
        name=cohort_in.name,
        course_id=cohort_in.course_id,
        instructor_id=current_user.id
    )
    db.add(new_cohort)
    await db.commit()
    await db.refresh(new_cohort)
    return new_cohort

@router.get("/cohorts/{cohort_id}", response_model=InstructorCohortResponse)
async def get_cohort(cohort_id: UUID, current_user: User = Depends(role_required("instructor", "admin")), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InstructorCohort)
        .options(selectinload(InstructorCohort.members))
        .where(InstructorCohort.id == cohort_id, InstructorCohort.instructor_id == current_user.id)
    )
    cohort = result.scalar_one_or_none()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    return cohort

@router.post("/cohorts/{cohort_id}/members", response_model=InstructorCohortResponse)
async def add_members(cohort_id: UUID, req: AddMembersRequest, current_user: User = Depends(role_required("instructor", "admin")), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InstructorCohort)
        .options(selectinload(InstructorCohort.members))
        .where(InstructorCohort.id == cohort_id, InstructorCohort.instructor_id == current_user.id)
    )
    cohort = result.scalar_one_or_none()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
        
    for u_id in req.user_ids:
        u_result = await db.execute(select(User).where(User.id == u_id))
        user = u_result.scalar_one_or_none()
        if user and user not in cohort.members:
            cohort.members.append(user)
            
    await db.commit()
    await db.refresh(cohort)
    return cohort

@router.get("/cohorts/{cohort_id}/analytics")
async def cohort_analytics(cohort_id: UUID, current_user: User = Depends(role_required("instructor", "admin")), db: AsyncSession = Depends(get_db)):
    # Basic stub
    return {"cohort_id": cohort_id, "average_mastery": 85.5, "active_students": 12}
