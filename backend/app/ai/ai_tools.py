import re

BASIC_INTENTS = {
    "wallet": ["رصيد", "محفظة", "تحويل", "سحب", "إيداع"],
    "travel": ["سفر", "تذكرة", "طيران", "رحلة", "search"],
    "help": ["مساعدة", "support", "help"],
}


def normalize_text(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9\u0600-\u06FF ]+", "", text.lower()).strip()


def classify_intent(text: str):
    for intent, keywords in BASIC_INTENTS.items():
        for k in keywords:
            if k in text:
                return intent, 0.92
    return "general", 0.55
