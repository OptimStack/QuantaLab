from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.db import get_db
from app.models.progress import Progress
from app.schemas.progress import ProgressResponse, ProgressUpdate
from app.utils.decorators import get_current_user
from app.models.user import User
from .adaptive import get_recommendation

router = APIRouter()

@router.get("/me", response_model=List[ProgressResponse])
async def get_my_progress(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Progress).where(Progress.user_id == current_user.id))
    return result.scalars().all()

@router.put("/{lesson_id}", response_model=ProgressResponse)
async def update_progress(lesson_id: UUID, progress_in: ProgressUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Progress).where(Progress.user_id == current_user.id, Progress.lesson_id == lesson_id))
    progress = result.scalar_one_or_none()
    
    if not progress:
        progress = Progress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            status=progress_in.status,
            time_spent_seconds=progress_in.time_spent_seconds
        )
        db.add(progress)
    else:
        progress.status = progress_in.status
        progress.time_spent_seconds += progress_in.time_spent_seconds
        
    await db.commit()
    await db.refresh(progress)
    return progress

@router.get("/recommendation")
async def recommendation(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_recommendation(current_user.id, db)
