# backend/app/ai/intent_router.py

from fastapi import HTTPException
from .ai_tools import classify_intent
from .openai_client import OpenAIClient


async def route_intent(user_message: str):
    """
    يقوم بتحليل نية المستخدم عبر خوارزمية محلية + GPT
    ثم يقرر أي وحدة من النظام يتم استدعاؤها.
    """

    # تحليل مبدئي محلي
    local = classify_intent(user_message)

    # لو الثقة ضعيفة نستخدم GPT
    if local.confidence < 0.75:
        gpt = OpenAIClient()
        ai_intent = await gpt.detect_intent(user_message)
        intent = ai_intent.intent
    else:
        intent = local.intent

    # التوجيه حسب النية
    if intent == "book_flight":
        return {"action": "search_flight", "message": "جارٍ البحث عن الرحلات…"}

    if intent == "wallet_status":
        return {"action": "wallet_balance", "message": "جاري جلب بيانات المحفظة"}

    if intent == "service_request":
        return {"action": "new_service_request", "message": "تم تسجيل طلب الخدمة"}

    # لو دردشة عامة
    if intent == "general_chat":
        gpt = OpenAIClient()
        reply = await gpt.chat(user_message)
        return {"action": "ai_chat", "reply": reply}

    raise HTTPException(status_code=400, detail="تعذّر تحديد نوع الطلب")
