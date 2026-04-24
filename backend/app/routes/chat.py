from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.orchestrate import (
    send_message_to_agent,
    create_session,
    delete_session,
)

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    volunteer_id: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    response: str
    agent_used: Optional[str] = None


@router.post("/", response_model=ChatResponse)
async def chat(body: ChatRequest):
    try:
        session_id = body.session_id or await create_session()

        result = await send_message_to_agent(
            session_id=session_id,
            message=body.message,
            volunteer_id=body.volunteer_id,
        )

        # Extrai texto da resposta do Orchestrate
        response_text = (
            result.get("output", {})
            .get("generic", [{}])[0]
            .get("text", "Desculpe, não consegui processar sua mensagem.")
        )

        return ChatResponse(
            session_id=session_id,
            response=response_text,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{session_id}")
async def end_session(session_id: str):
    await delete_session(session_id)
    return {"message": "Sessão encerrada com sucesso"}