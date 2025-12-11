import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_openai(message: str, intent: str) -> str:
    prompt = f"""
    You are ALFA — AI assistant for Daral Travel.
    User Intent: {intent}
    User Message: {message}
    Provide a natural helpful response.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
    )

    return response.choices[0].message["content"]
