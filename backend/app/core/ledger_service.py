from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.wallet import Wallet
from app.models.ledger import LedgerEntry


def apply_ledger_entry(
    db: Session,
    *,
    user_id: int,
    wallet_id: int,
    amount: Decimal,
    entry_type: str,
    currency: str = "USD",
    reference: str | None = None,
    admin_id: int | None = None,
):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise ValueError("Wallet not found")

    wallet.balance = wallet.balance + amount

    entry = LedgerEntry(
        user_id=user_id,
        wallet_id=wallet_id,
        amount=amount,
        entry_type=entry_type,
        currency=currency,
        reference=reference,
        created_by_admin_id=admin_id,
    )

    db.add(entry)
    db.commit()
    db.refresh(wallet)

    return wallet, entry
