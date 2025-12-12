def score_intent(payload: dict) -> str:
    """
    Rule-based + AI-safe intent scoring
    No decisions, no routing — tagging only
    """

    score = 0

    title = (payload.get("title") or "").lower()
    description = (payload.get("description") or "").lower()

    # Completeness
    if payload.get("city_from") or payload.get("city_to"):
        score += 1

    if payload.get("price_offer"):
        score += 2

    if len(description) > 20:
        score += 1

    # Strong buying signals
    strong_keywords = [
        "ready", "urgent", "confirm", "booking",
        "حجز", "جاهز", "مؤكد", "سريع"
    ]

    if any(k in title or k in description for k in strong_keywords):
        score += 2

    # Final classification
    if score >= 4:
        return "high"
    if score >= 2:
        return "medium"
    return "low"
