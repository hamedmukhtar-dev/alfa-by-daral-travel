from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from app.db import get_db
from app.models.offline_payment import OfflinePayment
from app.models.wallet import Wallet
from app.models.user import User

from app.core.security import get_current_user, require_admin
from app.core.ledger_service import apply_ledger_entry
from app.core.audit import log_admin_action
from app.config import settings

router = APIRouter(prefix="/offline-payments", tags=["Offline Payments"])


def _get_wallet(db: Session, user_id: int) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


# -----------------------------
# User: Create Offline Payment (Pilot Guarded)
# -----------------------------
@router.post("/create")
def create_offline_payment(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not settings.PILOT_MODE or not settings.ENABLE_OFFLINE_PAYMENTS:
        raise HTTPException(status_code=403, detail="Offline payments disabled")

    amount_raw = payload.get("amount")
    method = payload.get("method")
    reference = payload.get("reference")

    if amount_raw is None or method is None:
        raise HTTPException(status_code=400, detail="amount and method are required")

    try:
        amount = Decimal(str(amount_raw))
    except Exception:
        raise HTTPException(status_code=400, detail="invalid amount")

    if amount <= 0 or amount > Decimal(str(settings.MAX_OFFLINE_PAYMENT_AMOUNT)):
        raise HTTPException(status_code=400, detail="amount exceeds pilot limits")

    payment = OfflinePayment(
        user_id=current_user.id,
        amount=amount,
        method=method,
        reference=reference,
        status="pending",
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "message": "Offline payment submitted (pilot)",
        "payment_id": payment.id,
        "status": payment.status,
    }
