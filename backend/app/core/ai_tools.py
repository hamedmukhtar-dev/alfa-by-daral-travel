def normalize_text(text: str) -> str:
    """
    Clean input text before sending prompts to the AI model.
    """
    return text.strip().lower()


def build_intent_prompt(user_message: str) -> str:
    """
    Standardized ALFA intent-detection prompt.
    """
    return f"""
    Analyze the user message and return ONLY the action category.

    User message: "{user_message}"
    
    Categories:
    - travel_search
    - wallet_balance
    - wallet_transfer
    - service_request
    - help
    - unknown
    """
