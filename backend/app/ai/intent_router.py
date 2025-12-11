from app.ai.ai_tools import normalize_text, classify_intent


def detect_intent(text: str):
    clean = normalize_text(text)
    intent, confidence = classify_intent(clean)
    return intent, confidence
