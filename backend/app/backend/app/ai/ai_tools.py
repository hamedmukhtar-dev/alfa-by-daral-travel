# backend/app/ai/ai_tools.py

from pydantic import BaseModel
from typing import Optional, List

class IntentResult(BaseModel):
    intent: str
    confidence: float
    parameters: Optional[dict] = None


def classify_intent(user_message: str) -> IntentResult:
    message = user_message.lower()

    if "تذكرة" in message or "رحلة" in message:
        return IntentResult(intent="book_flight", confidence=0.88)

    if "رصيد" in message or "محفظة" in message:
        return IntentResult(intent="wallet_status", confidence=0.90)

    if "طلب" in message or "خدمة" in message:
        return IntentResult(intent="service_request", confidence=0.82)

    return IntentResult(intent="general_chat", confidence=0.60)
