import httpx
from ..config import settings


class OpenAIClient:
    """
    عميل بسيط لـ OpenAI. تقدر تطوره لاحقاً.
    هنا حاطين سكِلتون بس.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.OPENAI_API_KEY

    async def chat(self, messages: list[dict]) -> str:
        if not self.api_key:
            # في حالة عدم وجود مفتاح → نرجع رد ثابت عشان الـ dev
            return "AI is not configured yet. Please set OPENAI_API_KEY."

        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": "gpt-4.1-mini",
            "messages": messages,
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
