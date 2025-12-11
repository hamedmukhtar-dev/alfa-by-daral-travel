from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.ai import AIRequest, AIResponse
from app.ai.intent_router import detect_intent
from app.ai.openai_client import ask_openai
from app.db import get_db
from app.models.user import User
from app.core.security import get_current_user


router = APIRouter(prefix="/ai", tags=["ALFA Assistant"])


# -------------------------------
# AI ASSISTANT ENDPOINT
# -------------------------------
@router.post("/ask", response_model=AIResponse)
async def ask_alfa(
    payload: AIRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Step 1 — detect intent
    intent, confidence = detect_intent(payload.message)

    # Step 2 — generate AI reply (OpenAI)
    reply = ask_openai(message=payload.message, intent=intent)

    return AIResponse(
        reply=reply,
        intent=intent,
        confidence=confidence,
    )
