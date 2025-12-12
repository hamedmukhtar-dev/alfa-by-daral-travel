import logging

logger = logging.getLogger("alfa.notifications")


async def notify_high_intent(request):
    """
    Pilot notification hook.
    Currently logs only (safe).
    Can be extended to email/webhook/whatsapp later.
    """
    logger.warning(
        f"[HIGH INTENT] Request #{request.id} | "
        f"{request.title} | Phone: {request.user_phone}"
    )
