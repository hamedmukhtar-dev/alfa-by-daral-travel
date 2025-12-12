from sqlalchemy.ext.asyncio import AsyncSession
from app.models.alert import Alert


async def create_alert(
    db: AsyncSession,
    type: str,
    severity: str,
    message: str,
    source_id: int | None = None,
):
    alert = Alert(
        type=type,
        severity=severity,
        message=message,
        source_id=source_id,
    )
    db.add(alert)
    await db.commit()
    await db.refresh(alert)

    # Pilot-safe notification (log only)
    print(f"[ALERT:{severity.upper()}] {message}")

    return alert
