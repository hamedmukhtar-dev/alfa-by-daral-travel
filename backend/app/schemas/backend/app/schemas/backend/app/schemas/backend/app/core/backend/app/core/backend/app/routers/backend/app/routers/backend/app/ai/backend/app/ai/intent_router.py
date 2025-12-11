from .openai_client import OpenAIClient


async def route_request(service_type: str, payload: dict) -> dict:
    """
    هنا منطق بسيط:
    - حالياً يرجع نفس service_type
    - لاحقاً تقدر تستخدم OpenAI لتحليل النص الحر وتحديد نوع الخدمة.
    """
    # مثال مبسط جداً:
    return {
        "service_type": service_type,
        "payload": payload,
    }
