from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.models.progress import Progress
from app.models.assessment import Submission

async def compute_mastery_score(user_id: UUID, lesson_id: UUID, db: AsyncSession) -> float:
    # Example weighted formula from Section 5.11
    # weights: time_spent 10%, completion 30%, assessment 60%
    result = await db.execute(select(Progress).where(Progress.user_id == user_id, Progress.lesson_id == lesson_id))
    progress = result.scalar_one_or_none()
    
    if not progress:
        return 0.0
        
    completion_score = 100.0 if progress.status == "completed" else 50.0 if progress.status == "in_progress" else 0.0
    time_score = min(progress.time_spent_seconds / 600.0 * 100, 100.0) # cap at 10 mins
    
    # Get assessment scores
    # This is a simplification. Real implementation would join Assessments and Questions.
    sub_result = await db.execute(
        select(Submission).where(Submission.user_id == user_id)
    )
    submissions = sub_result.scalars().all()
    avg_score = sum(s.score or 0 for s in submissions) / len(submissions) if submissions else 0.0
    
    mastery = (time_score * 0.1) + (completion_score * 0.3) + (avg_score * 0.6)
    
    progress.mastery_score = mastery
    await db.commit()
    
    return mastery

async def get_recommendation(user_id: UUID, db: AsyncSession) -> dict:
    # Naive implementation
    result = await db.execute(select(Progress).where(Progress.user_id == user_id))
    all_progress = result.scalars().all()
    
    if not all_progress:
        return {"action": "start_course", "message": "Start the first lesson!"}
        
    for p in all_progress:
        mastery = p.mastery_score or 0.0
        if mastery < 50.0:
            return {"action": "review", "lesson_id": str(p.lesson_id), "message": "Review this lesson to improve your score."}
            
    return {"action": "proceed", "message": "You're doing great! Proceed to the next lesson."}
