import asyncio
from uuid import UUID
from datetime import datetime
from sqlalchemy import select
from app.db import SessionLocal
from app.models.assessment import Submission, Question, QuestionType
from app.assessments.grading import grade_mcq, grade_coding_challenge

async def _grade_submission(submission_id_str: str):
    async with SessionLocal() as db:
        sub_id = UUID(submission_id_str)
        result = await db.execute(select(Submission).where(Submission.id == sub_id))
        submission = result.scalar_one_or_none()
        if not submission:
            return
            
        q_result = await db.execute(select(Question).where(Question.id == submission.question_id))
        question = q_result.scalar_one_or_none()
        if not question:
            return
            
        if question.type == QuestionType.mcq:
            is_correct, score = grade_mcq(submission, question)
        else:
            is_correct, score = grade_coding_challenge(submission, question)
            
        submission.is_correct = is_correct
        submission.score = score
        submission.graded_at = datetime.utcnow()
        
        await db.commit()

def grade_submission_sync(submission_id: str):
    """Grade submission synchronously (for use with BackgroundTasks)."""
    asyncio.run(_grade_submission(submission_id))
