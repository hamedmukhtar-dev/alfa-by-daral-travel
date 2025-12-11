# backend/app/ai/intent_router.py

from fastapi import HTTPException
from .ai_tools import classify_intent
from .openai_client import OpenAIClient


async def route_intent(user_message: str):
    """
    يقوم بتحليل نية المستخدم عبر خوارزمية محلية + GPT
    ثم يقرر أي وحدة في النظام يتم استدعاؤها.
    """

    # الخطوة 1: تحليل مبدئي محلي
    local_intent = classify_intent(user_message)

    # الخطوة 2: إذا كانت الثقة ضعيفة — نستخدم GPT لتحديد النية
    if local_intent.confidence < 0.75:
        gpt = OpenAIClient()
        ai_intent = await gpt.detect_intent(user_message)
        intent = ai_intent.intent
    else:
        intent = local_intent.intent

    # الخطوة 3: التوجيه بناءً على النية
    if intent == "book_flight":
        return {"action": "search_flight", "message": "جارٍ البحث عن الرحلات…"}

    if intent == "wallet_status":
        return {"action": "wallet_balance", "message": "جاري جلب بيانات المحفظة"}

    if intent == "service_request":
        return {"action": "new_service_request", "message": "تم تسجيل طلب الخدمة"}

    # General Chat fallback
    if intent == "general_chat":
        gpt = OpenAIClient()
        reply = await gpt.chat(user_message)
        return {"action": "ai_chat", "reply": reply}

    raise HTTPException(status_code=400, detail="تعذّر تحديد نوع الطلب")
