# backend/app/ai/openai_client.py

import os
import httpx
from pydantic import BaseModel

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


class IntentResponse(BaseModel):
    intent: str
    confidence: float


class OpenAIClient:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY مفقود في ملف البيئة.")

    async def chat(self, message: str) -> str:
        """
        دردشة عامة عبر GPT
        """
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are ALFA AI Assistant."},
                {"role": "user", "content": message},
            ],
        }

        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(
                OPENAI_API_URL,
                json=payload,
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"}
            )

        data = res.json()
        return data["choices"][0]["message"]["content"]

    async def detect_intent(self, message: str) -> IntentResponse:
        """
        تحديد النية Intent عبر GPT
        """
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Return only intent name from: "
                        "book_flight, wallet_status, service_request, general_chat"
                    ),
                },
                {"role": "user", "content": message},
            ],
        }

        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(
                OPENAI_API_URL,
                json=payload,
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"}
            )

        reply = res.json()["choices"][0]["message"]["content"].lower()

        # simple mapping
        if "flight" in reply:
            return IntentResponse(intent="book_flight", confidence=0.9)
        if "wallet" in reply:
            return IntentResponse(intent="wallet_status", confidence=0.9)
        if "service" in reply:
            return IntentResponse(intent="service_request", confidence=0.9)

        return IntentResponse(intent="general_chat", confidence=0.6)
