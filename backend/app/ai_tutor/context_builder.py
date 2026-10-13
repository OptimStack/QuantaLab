from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.models.course import Lesson
from app.models.circuit import Circuit

async def build_context(mode: str, user_id: UUID, lesson_id: UUID = None, circuit_id: UUID = None, error_output: str = None, db: AsyncSession = None) -> str:
    context_parts = []
    
    if lesson_id and db:
        result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
        lesson = result.scalar_one_or_none()
        if lesson:
            context_parts.append(f"Current Lesson: {lesson.title}")
            context_parts.append(f"Concepts: {', '.join(lesson.concept_tags)}")
            context_parts.append(f"Lesson Content Snippet: {lesson.content_markdown[:500]}...")
            
    if circuit_id and db:
        result = await db.execute(select(Circuit).where(Circuit.id == circuit_id))
        circuit = result.scalar_one_or_none()
        if circuit:
            context_parts.append(f"Current Circuit Mode: {circuit.source_mode}")
            if circuit.source_mode == 'code' and circuit.source_code:
                context_parts.append(f"Code:\n```\n{circuit.source_code}\n```")
            else:
                context_parts.append(f"Gate Sequence: {circuit.gate_sequence_json}")
                
    if error_output:
        context_parts.append(f"Error Output:\n```\n{error_output}\n```")
        
    return "\n\n".join(context_parts)
