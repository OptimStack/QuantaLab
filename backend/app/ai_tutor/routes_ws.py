from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from app.db import SessionLocal
import json
from uuid import UUID

from app.models.ai_tutor_session import AiTutorSession, AiTutorMessage, RoleType, SessionMode
from .provider import get_provider
from .prompts import EXPLAIN_PROMPT, GENERATE_PROMPT, DEBUG_PROMPT, RECOMMEND_PROMPT
from .context_builder import build_context

router = APIRouter()

@router.websocket("/ws")
async def websocket_tutor(websocket: WebSocket):
    await websocket.accept()
    
    provider = get_provider()
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            mode_str = payload.get("mode", "explain")
            message = payload.get("message", "")
            user_id = payload.get("user_id")  # In real app, extract from token
            lesson_id = payload.get("lesson_id")
            circuit_id = payload.get("circuit_id")
            session_id = payload.get("session_id")
            error_output = payload.get("error_output")
            
            if not user_id:
                await websocket.send_text(json.dumps({"error": "user_id required"}))
                continue
                
            mode = SessionMode(mode_str)
            
            async with SessionLocal() as db:
                # Get or create session
                session = None
                if session_id:
                    result = await db.execute(select(AiTutorSession).where(AiTutorSession.id == UUID(session_id)))
                    session = result.scalar_one_or_none()
                    
                if not session:
                    session = AiTutorSession(
                        user_id=UUID(user_id),
                        lesson_id=UUID(lesson_id) if lesson_id else None,
                        circuit_id=UUID(circuit_id) if circuit_id else None
                    )
                    db.add(session)
                    await db.commit()
                    await db.refresh(session)
                    
                # Save user message
                user_msg = AiTutorMessage(
                    session_id=session.id,
                    role=RoleType.user,
                    mode=mode,
                    content=message
                )
                db.add(user_msg)
                await db.commit()
                
                # Build context
                context = await build_context(mode_str, UUID(user_id), 
                                           UUID(lesson_id) if lesson_id else None,
                                           UUID(circuit_id) if circuit_id else None,
                                           error_output, db)
                                           
                if mode == SessionMode.explain:
                    sys_prompt = EXPLAIN_PROMPT.format(context=context)
                elif mode == SessionMode.generate:
                    sys_prompt = GENERATE_PROMPT.format(context=context)
                elif mode == SessionMode.debug:
                    sys_prompt = DEBUG_PROMPT.format(context=context)
                else:
                    sys_prompt = RECOMMEND_PROMPT.format(context=context)
                    
                messages = [{"role": "user", "content": message}]
                
                full_response = ""
                async for chunk in provider.stream_completion(messages, sys_prompt):
                    full_response += chunk
                    await websocket.send_text(json.dumps({"chunk": chunk}))
                    
                await websocket.send_text(json.dumps({"done": True, "session_id": str(session.id)}))
                
                # Save assistant message
                assistant_msg = AiTutorMessage(
                    session_id=session.id,
                    role=RoleType.assistant,
                    mode=mode,
                    content=full_response
                )
                db.add(assistant_msg)
                await db.commit()

    except WebSocketDisconnect:
        pass
