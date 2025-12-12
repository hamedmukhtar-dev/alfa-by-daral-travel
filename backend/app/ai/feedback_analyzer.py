from app.ai.openai_client import ask_openai


async def analyze_feedback(message: str) -> dict:
    prompt = f"""
Analyze the following user feedback and return STRICT JSON only.

Feedback:
\"\"\"{message}\"\"\"

Return JSON with:
- category: complaint | suggestion | issue | praise | risk
- sentiment: positive | neutral | negative
- priority: high | medium | low
"""

    try:
        result = await ask_openai(prompt)
        return result
    except Exception:
        # Safe fallback
        return {
            "category": "issue",
            "sentiment": "neutral",
            "priority": "medium",
        }
