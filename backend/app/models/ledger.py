from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db import Base


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)

    entry_type = Column(String, nullable=False)
    # examples:
    # credit
    # debit
    # admin_adjustment
    # offline_payment
    # service_charge

    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String, default="USD")

    reference = Column(String, nullable=True)
    # service_request_id
    # offline_payment_id
    # manual_ref

    created_by_admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
