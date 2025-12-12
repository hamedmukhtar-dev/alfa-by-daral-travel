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

router = APIRouter(prefix="/offline-payments", tags=["Offline Payments"])


# -----------------------------
# Helpers
# -----------------------------
def _get_wallet(db: Session, user_id: int) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


# -----------------------------
# User: Create Offline Payment
# -----------------------------
@router.post("/create")
def create_offline_payment(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    payload = {
        "amount": 100,
        "method": "cash" | "bank_transfer",
        "reference": "receipt / note"
    }
    """
    amount_raw = payload.get("amount")
    method = payload.get("method")
    reference = payload.get("reference")

    if amount_raw is None or method is None:
        raise HTTPException(status_code=400, detail="amount and method are required")

    try:
        amount = Decimal(str(amount_raw))
    except Exception:
        raise HTTPException(status_code=400, detail="invalid amount")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="amount must be > 0")

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
        "message": "Offline payment submitted",
        "payment_id": payment.id,
        "status": payment.status,
    }


# -----------------------------
# Admin: Approve Offline Payment
# -----------------------------
@router.post("/admin/approve", dependencies=[Depends(require_admin)])
def approve_offline_payment(
    payload: dict,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_user),
):
    """
    payload = {
        "payment_id": 10
    }
    """
    payment_id = payload.get("payment_id")
    if payment_id is None:
        raise HTTPException(status_code=400, detail="payment_id is required")

    payment = db.query(OfflinePayment).filter(OfflinePayment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Offline payment not found")

    if payment.status != "pending":
        raise HTTPException(status_code=400, detail="Payment already processed")

    wallet = _get_wallet(db, payment.user_id)

    # Apply ledger credit
    wallet_after, entry = apply_ledger_entry(
        db,
        user_id=payment.user_id,
        wallet_id=wallet.id,
        amount=payment.amount,
        entry_type="offline_payment_credit",
        currency="USD",
        reference=f"offline_payment:{payment.id}",
        admin_id=admin_user.id,
    )

    # Update payment status
    payment.status = "approved"
    db.add(payment)
    db.commit()
    db.refresh(payment)

    # Audit
    log_admin_action(
        db,
        admin_id=admin_user.id,
        action="approve_offline_payment",
        target_type="offline_payment",
        target_id=payment.id,
        description=f"Approved offline payment amount={payment.amount} for user_id={payment.user_id}",
    )

    return {
        "message": "Offline payment approved",
        "payment_id": payment.id,
        "wallet": {
            "user_id": wallet_after.user_id,
            "balance": float(wallet_after.balance),
        },
        "ledger_entry_id": entry.id,
    }


# -----------------------------
# Admin: Reject Offline Payment
# -----------------------------
@router.post("/admin/reject", dependencies=[Depends(require_admin)])
def reject_offline_payment(
    payload: dict,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_user),
):
    """
    payload = {
        "payment_id": 10,
        "reason": "invalid receipt"
    }
    """
    payment_id = payload.get("payment_id")
    reason = payload.get("reason")

    if payment_id is None:
        raise HTTPException(status_code=400, detail="payment_id is required")

    payment = db.query(OfflinePayment).filter(OfflinePayment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Offline payment not found")

    if payment.status != "pending":
        raise HTTPException(status_code=400, detail="Payment already processed")

    payment.status = "rejected"
    db.add(payment)
    db.commit()
    db.refresh(payment)

    log_admin_action(
        db,
        admin_id=admin_user.id,
        action="reject_offline_payment",
        target_type="offline_payment",
        target_id=payment.id,
        description=reason or "Offline payment rejected",
    )

    return {
        "message": "Offline payment rejected",
        "payment_id": payment.id,
        "status": payment.status,
    }
