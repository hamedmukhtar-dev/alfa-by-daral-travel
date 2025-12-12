from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from app.db import get_db
from app.models.wallet import Wallet
from app.models.user import User

from app.core.security import get_current_user, require_admin
from app.core.ledger_service import apply_ledger_entry
from app.core.audit import log_admin_action

router = APIRouter(prefix="/wallet", tags=["Wallet"])


# -----------------------------
# Helpers
# -----------------------------
def _get_user_wallet(db: Session, user_id: int) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        wallet = Wallet(user_id=user_id, balance=0, pending_amount=0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet


# -----------------------------
# User endpoints
# -----------------------------
@router.get("/me")
def my_wallet(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    w = _get_user_wallet(db, current_user.id)
    return {
        "user_id": w.user_id,
        "balance": float(w.balance),
        "pending_amount": float(getattr(w, "pending_amount", 0)),
        "updated_at": getattr(w, "updated_at", None),
    }


@router.post("/request-offline-credit")
def request_offline_credit(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    User requests offline credit.
    This DOES NOT change balance.
    It only increases pending_amount waiting for admin approval.
    payload = {"amount": 100}
    """
    amount_raw = payload.get("amount")
    if amount_raw is None:
        raise HTTPException(status_code=400, detail="amount is required")

    try:
        amount = Decimal(str(amount_raw))
    except Exception:
        raise HTTPException(status_code=400, detail="invalid amount")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="amount must be > 0")

    w = _get_user_wallet(db, current_user.id)

    # pending only — no direct balance change
    w.pending_amount = (Decimal(str(getattr(w, "pending_amount", 0))) + amount)

    db.add(w)
    db.commit()
    db.refresh(w)

    return {
        "message": "Offline credit request submitted",
        "user_id": w.user_id,
        "pending_amount": float(w.pending_amount),
    }


# -----------------------------
# Admin endpoints (ENFORCED via Ledger)
# -----------------------------
@router.post("/admin/approve-offline-credit", dependencies=[Depends(require_admin)])
def admin_approve_offline_credit(
    payload: dict,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_user),
):
    """
    Admin approves user's pending credit:
    - Decrease pending_amount
    - Increase balance via LedgerEntry (apply_ledger_entry)
    payload = {"user_id": 12, "amount": 50, "reference": "offline_credit_approval"}
    """
    user_id = payload.get("user_id")
    amount_raw = payload.get("amount")
    reference = payload.get("reference")

    if user_id is None or amount_raw is None:
        raise HTTPException(status_code=400, detail="user_id and amount are required")

    try:
        amount = Decimal(str(amount_raw))
    except Exception:
        raise HTTPException(status_code=400, detail="invalid amount")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="amount must be > 0")

    w = _get_user_wallet(db, int(user_id))

    pending = Decimal(str(getattr(w, "pending_amount", 0)))
    if pending < amount:
        raise HTTPException(
            status_code=400,
            detail=f"insufficient pending_amount (pending={pending}, requested={amount})",
        )

    # reduce pending first (still not ledger)
    w.pending_amount = pending - amount
    db.add(w)
    db.commit()
    db.refresh(w)

    # NOW: balance update must go through ledger
    wallet, entry = apply_ledger_entry(
        db,
        user_id=w.user_id,
        wallet_id=w.id,
        amount=amount,  # credit
        entry_type="offline_credit",
        currency="USD",
        reference=reference or "offline_credit_approval",
        admin_id=admin_user.id,
    )

    # audit
    log_admin_action(
        db,
        admin_id=admin_user.id,
        action="approve_offline_credit",
        target_type="wallet",
        target_id=wallet.id,
        description=f"Approved offline credit for user_id={w.user_id}, amount={amount}",
    )

    return {
        "message": "Offline credit approved",
        "wallet": {
            "user_id": wallet.user_id,
            "balance": float(wallet.balance),
            "pending_amount": float(getattr(wallet, "pending_amount", 0)),
        },
        "ledger_entry_id": entry.id,
    }


@router.post("/admin/adjust", dependencies=[Depends(require_admin)])
def admin_adjust_balance(
    payload: dict,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_user),
):
    """
    Admin manual adjustment (credit/debit) via Ledger only.
    payload = {"user_id": 12, "amount": -10, "reference": "manual_fix"}
    Positive amount = credit
    Negative amount = debit
    """
    user_id = payload.get("user_id")
    amount_raw = payload.get("amount")
    reference = payload.get("reference")

    if user_id is None or amount_raw is None:
        raise HTTPException(status_code=400, detail="user_id and amount are required")

    try:
        amount = Decimal(str(amount_raw))
    except Exception:
        raise HTTPException(status_code=400, detail="invalid amount")

    if amount == 0:
        raise HTTPException(status_code=400, detail="amount must not be 0")

    w = _get_user_wallet(db, int(user_id))

    entry_type = "admin_adjustment_credit" if amount > 0 else "admin_adjustment_debit"

    wallet, entry = apply_ledger_entry(
        db,
        user_id=w.user_id,
        wallet_id=w.id,
        amount=amount,
        entry_type=entry_type,
        currency="USD",
        reference=reference or "admin_adjustment",
        admin_id=admin_user.id,
    )

    log_admin_action(
        db,
        admin_id=admin_user.id,
        action="admin_adjust_wallet",
        target_type="wallet",
        target_id=wallet.id,
        description=f"Admin adjusted wallet for user_id={w.user_id}, amount={amount}",
    )

    return {
        "message": "Wallet adjusted via ledger",
        "wallet": {
            "user_id": wallet.user_id,
            "balance": float(wallet.balance),
            "pending_amount": float(getattr(wallet, "pending_amount", 0)),
        },
        "ledger_entry_id": entry.id,
    }
